import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import re
import random
import math

from nova.utils.constant import EXCEPTION_LIST_BINANCE, VAR_NEEDED_FOR_POSITION, BINANCE_KLINES_COLUMNS

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


class BackTest:
    """
    This class helps for back testing a strategy.
    :parameter
        - candle : the candle size (ex: '15m')
        - list_pair : the list of pairs we want to back test (if None it will select all the pairs on Binance)
        - start : the starting day of the back test
        - end : the ending day of the back test
        - n_jobs : number of processes that will run in parallel when back testing pairs (default=8)
        - fees : fees applied by the exchange (0.04% for binance in taker)
        - max_pos : maximum number of position
    """

    def __init__(self,
                 candle: str,
                 list_pair,
                 start: datetime,
                 end: datetime,
                 fees: float,
                 max_pos: int,
                 amount_position: float = 100,
                 max_holding: int = 24):

        self.start_bk = 1000
        self.start = start
        self.end = end
        self.candle = candle
        self.fees = fees
        self.amount_per_position = amount_position
        self.list_pair = list_pair
        self.last_exit_date = np.nan
        self.max_pos = max_pos

        self.max_holding = max_holding

        self.exception_pair = EXCEPTION_LIST_BINANCE

        if type(self.list_pair).__name__ == 'str':
            raw_list_pair = self.get_list_pair()

            if self.list_pair.split()[0] == 'Random':
                nb_pairs = self.list_pair.split()[1]

                assert nb_pairs.isnumeric(), "Please enter valid list_pair"

                self.list_pair = random.choices(raw_list_pair, k=int(nb_pairs))

            elif self.list_pair != 'All pairs':
                raise Exception("Please enter valid list_pair")

            else:
                self.list_pair = raw_list_pair

        self.df_all_positions = {}
        self.df_pairs_stat = pd.DataFrame()
        self.df_pos = pd.DataFrame()

        df_freq = self.get_freq()

        self.df_pos['open_time'] = pd.date_range(start=start, end=end, freq=df_freq)
        for var in ['all_positions', 'total_profit_all_pairs', 'long_profit_all_pairs', 'short_profit_all_pairs']:
            self.df_pos[var] = 0

        self.df_copy = pd.DataFrame()
        self.position_cols = []
        self.df_all_pairs_positions = pd.DataFrame()

    def get_freq(self) -> str:
        if 'm' in self.candle:
            return self.candle.replace('m', 'min')
        else:
            return self.candle

    def _data_fomating(self, kline: list) -> pd.DataFrame:
        """
        Args:
            kline: is the list returned by get_historical_klines method from binance

        Returns: dataframe with usable format.
        """
        df = pd.DataFrame(kline, columns=BINANCE_KLINES_COLUMNS)
        num_var = [
            "open", "high", "low", "close", "volume", "quote_asset_volume",
            "nb_of_trades", "taker_base_volume", "taker_quote_volume"
        ]
        for var in num_var:
            df[var] = pd.to_numeric(df[var], downcast="float")

        df['timestamp'] = df['open_time']
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

        df['next_open'] = df['open'].shift(-1)

        return df

    def get_list_pair(self) -> list:
        """
        Returns:
            all the futures pairs we can to trade.
        """
        list_pair = []
        all_pair = self.client.futures_symbol_ticker()

        for pair in all_pair:
            if 'USDT' in pair['symbol'] and pair['symbol'] not in self.exception_pair:
                list_pair.append(pair['symbol'])

        return list_pair

    def get_all_historical_data(self,
                                pair: str,
                                market: str = 'futures') -> pd.DataFrame:
        """
        Args:
            market: spot or futures
            pair: string that represent the pair that has to be tested

        Returns:
            dataFrame that contain all the candles during the year entered for the wishing pair
            If the dataFrame had already been download we get the DataFrame from the csv file else, we are downloading
            all the data since 1st January 2017 to 1st January 2022.
        """

        if market == 'futures':
            get_klines = self.client.futures_historical_klines
        elif market == 'spot':
            get_klines = self.client.get_historical_klines
        else:
            raise Exception('Please enter a valid market (futures or market)')

        try:
            df = pd.read_csv(f'database/{market}/hist_{pair}_{self.candle}.csv')

            end_date_data = pd.to_datetime(df['timestamp'].max(), unit='ms')

            df['open_time'] = pd.to_datetime(df.open_time)
            df['close_time'] = pd.to_datetime(df.open_time)

            if self.end > end_date_data + timedelta(days=5):

                print("Update data: ", pair)
                klines = get_klines(pair,
                                    self.candle,
                                    end_date_data.strftime('%d %b, %Y'),
                                    self.end.strftime('%d %b, %Y'))

                new_df = self._data_fomating(klines)

                df = pd.concat([df, new_df])
                df = df.drop_duplicates(subset=['open_time'])

                df.to_csv(f'database/{market}/hist_{pair}_{self.candle}.csv', index=False)

            df = df.set_index('timestamp')
            return df[(df.open_time >= self.start) & (df.open_time <= self.end)]

        except:
            klines = get_klines(pair,
                               self.candle,
                               datetime(2018, 1, 1).strftime('%d %b, %Y'),
                               self.end.strftime('%d %b, %Y'))

            df = self._data_fomating(klines)

            df = df.dropna()

            df.to_csv(f'database/{market}/hist_{pair}_{self.candle}.csv', index=False)

            df = df.set_index('timestamp')

            return df[(df.open_time >= self.start) & (df.open_time <= self.end)]

    def get_exit_signals_date(self, x):
        """
        Note: The dataframe as to have exit_situation and index_num variable that is a boolean. It indicates when an
        Exit Signal is located in the timeseries

        Args:
            x: is the element of the apply method on a pandas dataframe
        Returns:
            It returns the closest date at which an execution of the exit is made
        """
        try:
            end_pt = x.index_num + self.convert_hours_to_candle_nb()
            closest_exit = np.where(self.df_copy['exit_situation'][x.index_num: end_pt] == True)[0][-1]
            if (closest_exit > 0) and (self.df_copy['all_entry_point'][x.index_num] != np.nan):
                return self.df_copy['open_time'][x.index_num + closest_exit]
            else :
                return np.datetime64('NaT')
        except:
            return np.datetime64('NaT')

    def create_all_exit_point(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Args:
            df:
        Returns:
        """
        all_exit_var = ['closest_sl', 'closest_tp', 'max_hold_date']

        if 'exit_signal_date' in df.columns:
            all_exit_var.append('exit_signal_date')

        df['all_exit_time'] = df[all_exit_var].min(axis=1)
        condition_exit_type_sl = (df.all_entry_point.notnull()) & (df['all_exit_time'] == df['closest_sl'])
        condition_exit_type_tp = (df.all_entry_point.notnull()) & (df['all_exit_time'] == df['closest_tp'])
        max_hold_date_sl = (df.all_entry_point.notnull()) & (df['all_exit_time'] == df['max_hold_date'])

        if 'exit_signal_date' in all_exit_var:
            condition_exit_strat = (df.all_entry_point.notnull()) & (df['all_exit_time'] == df['exit_signal_date'])
            df['all_exit_point'] = np.where(condition_exit_type_sl, -10,
                                            np.where(condition_exit_type_tp, 20,
                                                     np.where(max_hold_date_sl, 10,
                                                              np.where(condition_exit_strat, 5, np.nan))))
        else:
            df['all_exit_point'] = np.where(condition_exit_type_sl, -10,
                                            np.where(condition_exit_type_tp, 20,
                                                     np.where(max_hold_date_sl, 10, np.nan)))

        return df

    def create_all_tp_sl(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Args:
            df: dataframe that contains the 'all_entry_point' with the following properties:
                1 -> enter long position
                -1 -> enter short position
                nan -> no actions

        Returns:
            The function created 4 variables :
                all_entry_price, all_entry_time, all_tp, all_sl
        """

        df['all_entry_price'] = np.where(df.all_entry_point.notnull(), df.next_open, np.nan)
        df['all_entry_time'] = np.where(df.all_entry_point.notnull(), df.open_time, np.datetime64('NaT'))

        df['all_tp'] = np.where(df.all_entry_point == -1, df.all_entry_price * (1 - self.tp_prc),
                                np.where(df.all_entry_point == 1, df.all_entry_price * (1 + self.tp_prc), np.nan))

        df['all_sl'] = np.where(df.all_entry_point == -1, df.all_entry_price * (1 + self.sl_prc),
                                np.where(df.all_entry_point == 1, df.all_entry_price * (1 - self.sl_prc), np.nan))

        return df

    def convert_hours_to_candle_nb(self) -> int:
        multi = int(float(re.findall(r'\d+', self.candle)[0]))

        if 'm' in self.candle:
            return int(60 / multi * self.max_holding)
        if 'h' in self.candle:
            return int(1 / multi * self.max_holding)
        if 'd' in self.candle:
            return int(1 / (multi * 24) * self.max_holding)

    def create_closest_tp_sl(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        Args:
            df: dataframe that contains the variables all_entry_point, all_sl and all_tp

        Returns:
            the dataframe with 3 new variables closest_sl, closest_tp, max_hold_date

        """

        # create list of variables that we will have to drop
        lead_sl = []
        lead_tp = []

        # creating all leading variables

        nb_candle = self.convert_hours_to_candle_nb()

        for i in range(1, nb_candle + 1):
            condition_sl_long = (df.low.shift(-i) <= df.all_sl) & (df.all_entry_point == 1)
            condition_sl_short = (df.high.shift(-i) >= df.all_sl) & (df.all_entry_point == -1)
            condition_tp_short = (df.low.shift(-i) <= df.all_tp) & (df.high.shift(-i) <= df.all_sl) & (
                    df.all_entry_point == -1)
            condition_tp_long = (df.all_entry_point == 1) & (df.high.shift(-i) >= df.all_tp) & (
                    df.low.shift(-i) >= df.all_sl)

            df[f'sl_lead_{i}'] = np.where(condition_sl_long | condition_sl_short, df.open_time.shift(-i),
                                          np.datetime64('NaT'))
            df[f'tp_lead_{i}'] = np.where(condition_tp_short | condition_tp_long, df.open_time.shift(-i),
                                          np.datetime64('NaT'))
            lead_sl.append(f'sl_lead_{i}')
            lead_tp.append(f'tp_lead_{i}')

        # get the closest sl and tp
        df['closest_sl'] = df[lead_sl].min(axis=1)
        df['closest_tp'] = df[lead_tp].min(axis=1)

        # get the max holding date
        delta_holding = timedelta(hours=self.max_holding)
        df['max_hold_date'] = np.where(df.all_entry_point.notnull(), df['open_time'] + delta_holding, np.datetime64('NaT'))

        # clean dataset
        df.drop(lead_sl + lead_tp, axis=1, inplace=True)

        return df

    def create_position_df(self, df: pd.DataFrame, pair: str):
        """
        Args:
            df: timeseries dataframe that contains the following variables all_entry_time, all_entry_point,
            all_entry_price, all_exit_time, all_exit_point, all_tp, all_sl
            pair: pair that we are currently backtesting
        Returns:
        """

        # We keep only the important variables
        final_df = df[VAR_NEEDED_FOR_POSITION]

        # remove the missing values and reset index
        final_df = final_df.dropna()
        final_df.reset_index(drop=True, inplace=True)

        # create the variable that indicates if a transaction is good or not
        final_df['is_good'] = np.nan

        # For Loop in all the transaction (from the oldest to the newest)
        # determine if the transaction could have been executed
        for index, row in final_df.iterrows():
            good = True
            if index == 0:
                self.last_exit_date = row.all_exit_time
            elif row.all_entry_time <= pd.to_datetime(self.last_exit_date):
                good = False
            else:
                self.last_exit_date = row.all_exit_time

            final_df.loc[index, 'is_good'] = good

        # keep only the real transaction that can be executed
        final_df = final_df[final_df['is_good']]
        final_df = final_df.drop('is_good', axis=1)
        final_df.reset_index(drop=True, inplace=True)

        # add back the 'next_open' variable
        final_df = pd.merge(final_df, df[['open_time', 'next_open']], how="left",
                            left_on=["all_exit_time"], right_on=["open_time"])
        final_df = final_df.drop('open_time', axis=1)

        # compute the exit price for depending on the exit point category
        final_df['exit_price'] = np.where(final_df['all_exit_point'] == -10, final_df['all_sl'],
                                          np.where(final_df['all_exit_point'] == 20, final_df['all_tp'],
                                                   final_df['next_open']))

        # removing non important variables and renaming columns
        final_df = final_df.drop(['all_sl', 'all_tp', 'next_open'], axis=1)
        final_df = final_df.rename(columns={
            'all_entry_time': 'entry_time',
            'all_entry_point': 'entry_point',
            'all_entry_price': 'entry_price',
            'all_exit_time': 'exit_time',
            'all_exit_point': 'exit_point'
        })

        final_df = self.compute_profit(final_df)

        self.df_all_positions[pair] = final_df

    def compute_profit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Args:
            df: dataframe of all the positions that has to contain the following variables
            exit_time, entry_time, exit_price, entry_price, entry_point

        Returns:
            a dataframe with new variables 'nb_minutes_in_position', 'prc_not_realized',
            'amt_not_realized', 'tx_fees_paid', 'PL_amt_realized', 'PL_prc_realized',
            'next_entry_time'
        """
        df['nb_minutes_in_position'] = (df.exit_time - df.entry_time).astype('timedelta64[m]')

        df['prc_not_realized'] = (df['entry_point'] * (df['exit_price'] - df['entry_price']) / df['entry_price'])
        df['amt_not_realized'] = df['prc_not_realized'] * self.amount_per_position

        df['tx_fees_paid'] = (2 * self.amount_per_position + df['amt_not_realized']) * self.fees

        df['PL_amt_realized'] = df['amt_not_realized'] - df['tx_fees_paid']
        df['PL_prc_realized'] = df['PL_amt_realized'] / self.amount_per_position

        df['next_entry_time'] = df.entry_time.shift(-1)
        df['minutes_bf_next_position'] = (df.next_entry_time - df.exit_time).astype('timedelta64[m]')

        df.drop(['prc_not_realized', 'amt_not_realized', 'next_entry_time'], axis=1, inplace=True)

        return df

    def create_full_positions(self, df: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Args:
            df: it's the position dataframes with all the statistics per positions
            pair: is the string that represents the pair that is currently backtest

        Returns:
            recreates the real time series scenario when a position has been taken.
        """

        # create entering and exiting dataset
        entering = df[['entry_time', 'entry_point']]
        exiting = df[['exit_time', 'exit_point', 'PL_amt_realized']]

        # add to the main dataframe the 'entry_point', 'PL_amt_realized' and 'exit_point'
        self.df_pos = pd.merge(
            self.df_pos,
            entering,
            how='left',
            left_on='open_time',
            right_on='entry_time')

        self.df_pos = pd.merge(
            self.df_pos, exiting,
            how='left',
            left_on='open_time',
            right_on='exit_time')

        # create the in position variable and forward fill it
        condition_enter = self.df_pos['entry_point'].notnull()
        condition_exit = self.df_pos['exit_point'].notnull()

        self.df_pos[f'in_position_{pair}'] = np.where(condition_enter, self.df_pos['entry_point'],
                                                      np.where(condition_exit, 0, np.nan))
        self.df_pos[f'in_position_{pair}'] = self.df_pos[f'in_position_{pair}'].fillna(method='ffill').fillna(0)

        self.df_pos['all_positions'] = self.df_pos['all_positions'] + self.df_pos[f'in_position_{pair}'].abs()

        # Create the cumulative total profit for the pair
        self.df_pos[f'PL_amt_realized_{pair}'] = self.df_pos['PL_amt_realized'].fillna(0)
        self.df_pos[f'total_profit_{pair}'] = self.df_pos[f'PL_amt_realized_{pair}'].cumsum()

        condition_long_pl = (self.df_pos[f'in_position_{pair}'] == 0) & (
                self.df_pos[f'in_position_{pair}'].shift(1) == 1)
        condition_short_pl = (self.df_pos[f'in_position_{pair}'] == 0) & (
                self.df_pos[f'in_position_{pair}'].shift(1) == -1)

        # add the long profit and short profit for plot
        self.df_pos['Long_PL_amt_realized'] = np.where(condition_long_pl, self.df_pos['PL_amt_realized'], 0)
        self.df_pos[f'long_profit_{pair}'] = self.df_pos['Long_PL_amt_realized'].cumsum()
        self.df_pos['Short_PL_amt_realized'] = np.where(condition_short_pl, self.df_pos['PL_amt_realized'], 0)
        self.df_pos[f'short_profit_{pair}'] = self.df_pos['Short_PL_amt_realized'].cumsum()

        # clean the variables not needed
        to_drop = ['Short_PL_amt_realized', 'Long_PL_amt_realized', f'PL_amt_realized_{pair}', 'PL_amt_realized',
                   'entry_time', 'entry_point', 'exit_time', 'exit_point']
        self.df_pos.drop(to_drop, axis=1, inplace=True)

        # update the bot total profit or all token
        self.df_pos['total_profit_all_pairs'] = self.df_pos['total_profit_all_pairs'] + self.df_pos[f'total_profit_{pair}']
        self.df_pos['long_profit_all_pairs'] = self.df_pos['long_profit_all_pairs'] + self.df_pos[f'long_profit_{pair}']
        self.df_pos['short_profit_all_pairs'] = self.df_pos['short_profit_all_pairs'] + self.df_pos[f'short_profit_{pair}']

    def get_performance_graph(self, pair: str):
        """
        Args:
            pair: string that represents the pair.
        Returns:
            Creates the plots with the total return, long return and short return
        """
        plt.figure(figsize=(10, 10))
        plt.plot(self.df_pos.open_time, self.df_pos[f'total_profit_{pair}'], label='Total Profit')
        plt.plot(self.df_pos.open_time, self.df_pos[f'long_profit_{pair}'], label='Long Profit')
        plt.plot(self.df_pos.open_time, self.df_pos[f'short_profit_{pair}'], label='Short Profit')
        plt.legend()
        plt.title(f"Backtest {self.strategy_name} strategy for {pair}")
        plt.show()

    def get_pair_stats(self, df: pd.DataFrame, pair: str) -> pd.DataFrame:
        """
        Args:
            df : position dataframe that contains all the statistics needed
            pair : string representing the pair we are currently backtesting
        Returns:
            aggregated statistics to evaluate the current strategy and add it to
            df_stat  dataframe
        """

        # create long and short dataframe
        position_stat = {
            'long': df[df['entry_point'] == 1].reset_index(drop=True),
            'short': df[df['entry_point'] == -1].reset_index(drop=True)
        }

        # create tp, sl, es, ew dataframes
        exit_stat = {
            'tp': df[df['exit_point'] == 20].reset_index(drop=True),
            'sl': df[df['exit_point'] == -10].reset_index(drop=True),
            'es': df[df['exit_point'] == 5].reset_index(drop=True),
            'ew': df[df['exit_point'] == 10].reset_index(drop=True)
        }

        # create an empty dictionary
        perf_dict = dict()
        perf_dict['pair'] = pair

        # add general statistics
        perf_dict['total_position'] = len(df)
        perf_dict['avg_minutes_in_position'] = df['nb_minutes_in_position'].mean()
        perf_dict['total_profit_amt'] = df['PL_amt_realized'].sum()
        perf_dict['total_profit_prc'] = df['PL_prc_realized'].sum()
        perf_dict['total_tx_fees'] = df['tx_fees_paid'].sum()
        perf_dict['avg_minutes_before_next_position'] = df['minutes_bf_next_position'].mean()
        perf_dict['max_minutes_without_position'] = df['minutes_bf_next_position'].max()
        perf_dict['min_minutes_without_position'] = df['minutes_bf_next_position'].min()
        perf_dict['perc_winning_trade'] = len(df[df.PL_amt_realized > 0]) / len(df)
        perf_dict['avg_profit'] = df['PL_prc_realized'].sum() / len(df)

        # add statistics per type of positions
        for pos, pos_df in position_stat.items():
            perf_dict[f'nb_{pos}_position'] = len(pos_df)
            perf_dict[f'nb_tp_{pos}'] = len(pos_df[pos_df['exit_point'] == 20])
            perf_dict[f'nb_sl_{pos}'] = len(pos_df[pos_df['exit_point'] == -10])
            perf_dict[f'nb_exit_{pos}'] = len(pos_df[pos_df['exit_point'] == 5])
            perf_dict[f'nb_ew_{pos}'] = len(pos_df[pos_df['exit_point'] == 20])

            perf_dict[f'{pos}_profit_amt'] = pos_df['PL_amt_realized'].sum()
            perf_dict[f'{pos}_profit_prc'] = pos_df['PL_prc_realized'].sum()
            perf_dict[f'avg_minutes_in_{pos}'] = pos_df['nb_minutes_in_position'].mean()

        # add statistics per type of exit
        for ext, ext_df in exit_stat.items():
            perf_dict[f'nb_{ext}'] = len(ext_df)
            perf_dict[f'avg_minutes_before_{ext}'] = ext_df['nb_minutes_in_position'].mean()

        # add the statistics to the general stats df_stat
        stat_perf = pd.DataFrame([perf_dict], columns=list(perf_dict.keys()))
        self.df_pairs_stat = pd.concat([self.df_pairs_stat, stat_perf])

    def compute_geometric_profits(self,
                             row,
                             bankroll_evolution):

        actual_bankroll = bankroll_evolution[row.entry_time]

        row['position_size'] = actual_bankroll * self.positions_size
        row['PL_amt_realized'] = row['position_size'] * row['PL_prc_realized']

        return row

    def all_pairs_position(self):
        ############################# Create self.df_all_pairs_positions #############################

        since = self.start

        for pair in self.df_all_positions.keys():
            df_concat = self.df_all_positions[pair]
            df_concat['pair'] = pair
            self.df_all_pairs_positions = pd.concat([self.df_all_pairs_positions, self.df_all_positions[pair]])

        self.df_all_pairs_positions = self.df_all_pairs_positions[self.df_all_pairs_positions['entry_time'] > since]

        self.df_all_pairs_positions = self.df_all_pairs_positions.sort_values(by=['exit_time'])

        self.df_all_pairs_positions['position_size'] = self.positions_size * self.start_bk

        ##################### Shift all TP or SL exit time bc it is based on the open ################

        hours_step = self.max_holding / self.convert_hours_to_candle_nb()

        self.df_all_pairs_positions['exit_time'] = np.where(self.df_all_pairs_positions['exit_point'] == 20,
                                                            self.df_all_pairs_positions['exit_time'] + timedelta(
                                                                hours=hours_step),
                                                            self.df_all_pairs_positions['exit_time'])

        self.df_all_pairs_positions['exit_time'] = np.where(self.df_all_pairs_positions['exit_point'] == -10,
                                                            self.df_all_pairs_positions['exit_time'] + timedelta(
                                                                hours=hours_step),
                                                            self.df_all_pairs_positions['exit_time'])

        #############################      Delete impossible trades      #############################

        t = since
        actual_nb_pos = 0
        exit_times = []
        all_rows_to_delete = pd.DataFrame(columns=self.df_all_pairs_positions.columns)
        new_bk = self.start_bk
        bankroll_evolution = {self.start: self.start_bk}

        while t <= self.end:

            if t in exit_times:
                actual_nb_pos -= exit_times.count(t)
                exit_times = list(filter(t.__ne__, exit_times))

            entry_t = self.df_all_pairs_positions[self.df_all_pairs_positions['entry_time'] == t]
            nb_signals = entry_t.shape[0]

            # Delete rows if actual_nb_pos is over maximum pos
            if nb_signals + actual_nb_pos > self.max_pos:
                nb_to_delete = nb_signals - (self.max_pos - actual_nb_pos)

                rows_to_delete = entry_t.sample(n=nb_to_delete)

                self.df_all_pairs_positions = pd.concat([self.df_all_pairs_positions, rows_to_delete])
                self.df_all_pairs_positions = self.df_all_pairs_positions.drop_duplicates(keep=False)

                all_rows_to_delete = pd.concat([all_rows_to_delete, rows_to_delete])
                actual_nb_pos = self.max_pos

                # Append exit times
                real_entry_t = self.df_all_pairs_positions[self.df_all_pairs_positions['entry_time'] == t]
                new_bk = (1 + real_entry_t['PL_prc_realized'].sum() * self.positions_size) * bankroll_evolution[t]
                exit_times += real_entry_t['exit_time'].tolist()

            elif nb_signals != 0:

                actual_nb_pos += nb_signals

                # Append exit times
                real_entry_t = self.df_all_pairs_positions[self.df_all_pairs_positions['entry_time'] == t]
                new_bk = (1 + real_entry_t['PL_prc_realized'].sum() * self.positions_size) * bankroll_evolution[t]
                exit_times += real_entry_t['exit_time'].tolist()

            t = t + timedelta(hours=hours_step)

            bankroll_evolution[t] = new_bk

            assert new_bk > 0, f"You'd have been broke at {t}"

        if self.geometric_sizes:
            self.df_all_pairs_positions = self.df_all_pairs_positions.apply(lambda row: self.compute_geometric_profits(row,
                                                                                                                       bankroll_evolution),
                                                                            axis=1)
        else:
            self.df_all_pairs_positions['PL_amt_realized'] = self.df_all_pairs_positions['position_size'] *\
                                                             self.df_all_pairs_positions['PL_prc_realized']

        self.df_all_pairs_positions['cumulative_profit'] = self.df_all_pairs_positions['PL_amt_realized'].cumsum()

        self.df_all_pairs_positions['bankroll_size'] = self.df_all_pairs_positions['cumulative_profit'] + self.start_bk

        self.df_all_pairs_positions['tx_fees_paid'] = self.df_all_pairs_positions['position_size'] * self.fees \
                                                      * (2 + self.df_all_pairs_positions['PL_prc_realized'])

        for pair in self.list_pair:
            self.df_all_positions[pair] = self.df_all_pairs_positions[self.df_all_pairs_positions['pair'] == pair]

        ############################# Create full position for all pairs #############################

        for pair in self.list_pair:
            self.create_full_positions(df=self.df_all_positions[pair],
                                       pair=pair)
            self.get_pair_stats(df=self.df_all_positions[pair],
                                pair=pair)

    def compute_daily_return(self,
                             row,
                             df_all_pairs_positions):

        all_exit_of_the_day = df_all_pairs_positions[df_all_pairs_positions['exit_time'] <= row.date + timedelta(days=1)]
        all_exit_of_the_day = all_exit_of_the_day[all_exit_of_the_day['exit_time'] > row.date]

        if all_exit_of_the_day['bankroll_size'].values.shape[0] > 0:
            day_profit = 100 * (
                        all_exit_of_the_day['bankroll_size'].values[-1] - all_exit_of_the_day['bankroll_size'].values[
                    0]) / \
                         all_exit_of_the_day['bankroll_size'].values[0]
        else:
            day_profit = 0

        row['daily_percentage_profit'] = day_profit

        if all_exit_of_the_day.shape[0] > 0:
            row['bankroll'] = all_exit_of_the_day['bankroll_size'].values[-1]

        return row

    def compute_drawdown(self,
                        row,
                        df_daily):

        temp = df_daily[df_daily['date'] <= row.date]

        temp = temp[temp['date'] >= temp['bankroll'].idxmax()]

        row['drawdown'] = (temp['bankroll'].max() - row.bankroll) / temp['bankroll'].max()

        row['last_date_max'] = temp['bankroll'].idxmax()

        row['nb_day_since_last_date_max'] = (row.date - row['last_date_max']).days

        return row

    def create_full_statistics(self,
                               since: datetime):

        df_all_pairs_positions = self.df_all_pairs_positions[self.df_all_pairs_positions['entry_time'] > since]

        ################################ Create daily results df ######################

        first_day = since - timedelta(hours=since.hour, minutes=since.minute)
        last_day = self.end - timedelta(hours=self.end.hour, minutes=self.end.minute, microseconds=self.end.microsecond)

        df_daily = pd.DataFrame(index=pd.date_range(first_day, last_day), columns=['daily_percentage_profit',
                                                                                   'last_date_max'])
        df_daily['date'] = df_daily.index
        df_daily['bankroll'] = np.nan
        df_daily['drawdown'] = 0

        df_daily = df_daily.apply(lambda row: self.compute_daily_return(row, df_all_pairs_positions), axis=1)
        # fillna for days without exits
        df_daily['daily_percentage_profit'] = df_daily['daily_percentage_profit'].fillna(0)
        df_daily['bankroll'] = df_daily['bankroll'].fillna(method='ffill')
        df_daily['bankroll'] = df_daily['bankroll'].fillna(self.start_bk)

        df_daily = df_daily.apply(lambda row: self.compute_drawdown(row, df_daily), axis=1)

        ################################ Compute overview #############################

        overview = {}

        realized_profit = round(df_all_pairs_positions['PL_amt_realized'].sum(), 1)
        overview['Realized profit'] = f"{realized_profit} $"

        avg_profit = round(df_all_pairs_positions['PL_amt_realized'].mean(), 2)
        overview['Average profit / trade'] = f"{avg_profit} $"

        avg_profit_perc = round(100 * df_all_pairs_positions['PL_prc_realized'].mean(), 2)
        overview['Average profit / trade (%)'] = f"{avg_profit_perc} %"

        avg_profit_winning_trade = df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] > 0]['PL_amt_realized'].sum() / \
                                   df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] > 0].shape[0]

        avg_profit_perc_winning_trade = df_all_pairs_positions[df_all_pairs_positions['PL_prc_realized'] > 0]['PL_prc_realized'].sum() / \
                                        df_all_pairs_positions[df_all_pairs_positions['PL_prc_realized'] > 0].shape[0]

        avg_loss_losing_trade = df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] < 0]['PL_amt_realized'].sum() / \
                                df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] < 0].shape[0]

        avg_profit_perc_losing_trade = df_all_pairs_positions[df_all_pairs_positions['PL_prc_realized'] < 0]['PL_prc_realized'].sum() / \
                                        df_all_pairs_positions[df_all_pairs_positions['PL_prc_realized'] < 0].shape[0]

        overview['Average profit / winning trade'] = f"{round(avg_profit_winning_trade, 2)} $"
        overview['Average profit / winning trade (%)'] = f"{round(100 * avg_profit_perc_winning_trade, 2)} %"

        overview['Average loss / losing trade'] = f"{round(avg_loss_losing_trade, 2)} $"
        overview['Average profit / losing trade (%)'] = f"{round(100 * avg_profit_perc_losing_trade, 2)} %"

        best_profit = round(df_all_pairs_positions['PL_amt_realized'].max(), 2)
        overview['Best trade profit'] = f"{best_profit} $"
        worst_loss = round(df_all_pairs_positions['PL_amt_realized'].min(), 2)
        overview['Worst trade loss'] = f"{worst_loss} $"

        overview['Cumulative fees paid'] = f"{round(df_all_pairs_positions['tx_fees_paid'].sum(), 2)} $ "

        overview['Nb winning trade'] = df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] > 0].shape[0]
        overview['Nb losing trade'] = df_all_pairs_positions[df_all_pairs_positions['PL_amt_realized'] < 0].shape[0]

        overview['Total nb trade'] = overview['Nb losing trade'] + overview['Nb winning trade']

        overview['% winning trade'] = f"{round(100 * overview['Nb winning trade'] / overview['Total nb trade'], 1)} %"

        overview['Best day profit'] = f"{round(df_daily['daily_percentage_profit'].max(), 1)} %"

        overview['Worst day loss'] = f"{round(df_daily['daily_percentage_profit'].min(), 1)} %"

        overview['Max Nb Days Underwater'] = df_daily['nb_day_since_last_date_max'].max()

        ################################ Compute statistics #############################

        statistics = {}

        # Compute Geometric Returns
        total_return = 100 * realized_profit / self.start_bk

        statistics['Total return'] = f"{round(total_return, 2)} %"

        nb_days_backtest = (self.end - since).days
        geometric_return = 100 * ((1 + total_return / 100) ** (365 / (nb_days_backtest)) - 1)

        statistics['Geometric return (yearly)'] = f"{round(geometric_return, 2)} %"

        # Compute Volatility
        df_daily['Distribution'] = np.square(df_daily['daily_percentage_profit'] -
                                             df_daily['daily_percentage_profit'].mean())
        volatility = math.sqrt(df_daily['Distribution'].sum() / df_daily.shape[0])
        volatility = volatility * math.sqrt(365)

        statistics['Annualized standard deviation'] = f"{round(volatility, 2)} %"

        # Compute Sharpe Ratio
        sharpe_ratio = geometric_return / volatility

        statistics['Sharpe Ratio'] = round(sharpe_ratio, 2)

        # Compute Sortino Ratio
        df_down = df_daily[df_daily['daily_percentage_profit'] < 0].copy()
        df_down['Downside_distribution'] = np.square(df_down['daily_percentage_profit'] -
                                                     df_down['daily_percentage_profit'].mean())
        downside_volatility = math.sqrt(df_down['Downside_distribution'].sum() / df_daily.shape[0])
        downside_volatility = downside_volatility * math.sqrt(365)

        statistics['Downside volatility'] = f"{round(downside_volatility, 2)} %"

        sortino_ratio = geometric_return / downside_volatility
        statistics['Sortino Ratio'] = round(sortino_ratio, 2)

        statistics['Max DrawDown'] = f"{round(100 * df_daily['drawdown'].max(), 2)} %"
        start_max_DD = df_daily[df_daily['date'] == df_daily['drawdown'].idxmax()]['last_date_max']
        end_max_DD = df_daily[df_daily['date'] == df_daily['drawdown'].idxmax()]['date']

        statistics['Max DrawDown start'] = str(pd.to_datetime(start_max_DD.values[0]).date())
        statistics['Max DrawDown end'] = str(pd.to_datetime(end_max_DD.values[0]).date())

        ################################  Print statistics  #############################

        print("#" * 65)
        print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', 'Overview:', '|', '     ', '#'))
        print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', f'From {since.strftime("%Y-%m-%d")}', '|', 'Value', '#'))
        print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', f'To {self.end.strftime("%Y-%m-%d")}', '|', '     ', '#'))
        print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', f"With {self.start_bk} $ starting", '|', '     ', '#'))
        print("#" * 65)
        for k, v in overview.items():
            print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', k, '|', v, '#'))
            print("#", "-" * 61, "#")
        print("#" * 65)

        print("#" * 65)
        print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', 'Statistics:', '|', 'Value', '#'))
        print("#" * 65)
        for k, v in statistics.items():
            print("{:<5} {:<35} {:<5} {:<15} {:<1}".format('#', k, '|', v, '#'))
            print("#", "-" * 61, "#")
        print("#" * 65)

        all_statistics = {"overview": overview,
                          "statistics": statistics}

        return all_statistics

    def save_trades_charts(self,
                           data: pd.DataFrame,
                           perf: pd.DataFrame,
                           timedelta_before_entry: timedelta,
                           max_nb_chart: int,
                           pair: str):
        """
        This method will create the candle charts of all trades in perf. It will display the entry point and the exit
        price.

        Args:
            data: dataframe that contains all the candles OHLC
            perf: dataframe with all the positions
            timedelta_before_entry: the amount of time we want to look back before the entry signal
            max_nb_chart: maximum number of charts that we create
            pair: bah la pair hoa
        """

        position_type = {1: {'color': 'g', 'marker': '^', 'y': 'low'},
                         -1: {'color': 'r', 'marker': 'v', 'y': 'high'}}

        chart_id = 0

        for index, row in perf.iterrows():
            try:
                entry_date = row['entry_time']
                exit_price = row['exit_price']
                type = row['entry_point']

                trade_data = data[data.index >= (entry_date - timedelta_before_entry)].copy(deep=True)
                trade_data = trade_data[trade_data.index <= (entry_date + timedelta(hours=self.max_holding))]

                trade_data['all_entry_point'] = np.where(trade_data.index == entry_date, 1, np.nan)

                entry_signal = trade_data['all_entry_point'].abs() * trade_data[position_type[type]['y']]

                ap0 = [mpf.make_addplot(trade_data['ichimoku_a'], color='g'),
                       mpf.make_addplot(trade_data['ichimoku_b'], color='r'),
                       mpf.make_addplot(entry_signal, type='scatter', markersize=100,
                                        color=position_type[type]['color'],
                                        marker=position_type[type]['marker'])]

                name = pair + '_' + str(entry_date)

                mpf.plot(trade_data, type='candle', figratio=(7, 5), addplot=ap0,
                         hlines=dict(hlines=[exit_price], colors=[position_type[(-1) * type]['color']], linewidths=1,
                                     alpha=0.4),
                         savefig=f'./strategies/ichimoku/trade_charts/{name}.png', volume=False)

                chart_id += 1
                if chart_id > max_nb_chart:
                    return 0

            except Exception as e:
                print(e)
                continue

    def run_backtest(self, save: bool = True):

        """

        Args:
            save: bool
            save_chart: bool

        RUN BACK TEST !
        """

        i = 0
        while i < len(self.list_pair):
            pair = self.list_pair[i]

            try:
                print(f'BACK TESTING {pair}', "\U000023F3", end="\r")

                data = self.get_all_historical_data(pair)

                indicator_df = self.build_indicators(data)

                entry_df = self.entry_strategy(indicator_df)

                exit_df = self.exit_strategy(entry_df)

                self.create_position_df(exit_df, pair)

                print(f'BACK TESTING {pair}', "\U00002705")

            except Exception as e:
                print(f'BACK TESTING {pair}', "\U0000274C")

                self.list_pair.remove(pair)
                continue

            i += 1

        # Keep only positions such that number of pos < max nb positions
        print(f'Creating all positions and timeserie graph', "\U000023F3", end="\r")
        self.all_pairs_position()
        print(f'Creating all positions and timeserie graph', "\U00002705")

        print(f'Computing statistics', "\U000023F3", end="\r")
        all_statistics = self.create_full_statistics(since=self.start)
        print(f'Computing statistics', "\U00002705")

        self.get_performance_graph('all_pairs')

        if save:
            self.df_pairs_stat.to_csv(f'database/analysis/{self.strategy_name}/pairs_analytics.csv',
                                      index=False)

            with open(f'database/analysis/{self.strategy_name}/all_statistics.json', 'w') as fp:
                json.dump(all_statistics, fp)

        return all_statistics


