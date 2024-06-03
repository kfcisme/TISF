import pandas as pd
import numpy as np
from scipy.stats import pearsonr, linregress, norm

class max_player:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self, table_name):
        query = f"SELECT timestamp, player_id FROM {table_name}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_total_players(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_total_players = df.drop_duplicates(subset=['timestamp', 'player_id']).groupby('timestamp').size().reset_index(name='total_players')
        return daily_total_players

    def weekly_avg_total_players(self, daily_total_players):
        daily_total_players['week'] = pd.to_datetime(daily_total_players['timestamp']).dt.to_period('M')
        weekly_average_players = daily_total_players.groupby('week')['total_players'].mean().reset_index()
        weekly_average_players['week'] = weekly_average_players['week'].dt.to_timestamp()
        weekly_average_players = ['week', 'average_players', 'total_players']
        return weekly_average_players


    def insert_daily_total_players(self, daily_total_players):
        query = f"INSERT INTO {table名稱} (date, total_players) VALUES (%s, %s)"
        for index, row in daily_total_players.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['total_players']))

    def insert_weekly_average_players(self, weekly_average_players):
        query = f"INSERT INTO {table名稱} (week, average_players) VALUES (%s, %s)"
        for index, row in weekly_average_players.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['total_players']))

class peak_hour:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self, table_name):
        query = f"SELECT timestamp, player_id FROM {table_name}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_total_players(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_total_players = df.drop_duplicates(subset=['timestamp', 'player_id']).groupby('timestamp').size().reset_index(name='total_players')
        return daily_total_players

    def weekly_avg_total_players(self, daily_total_players):
        daily_total_players['week'] = pd.to_datetime(daily_total_players['timestamp']).dt.to_period('M')
        weekly_average_players = daily_total_players.groupby('week')['total_players'].mean().reset_index()
        weekly_average_players['week'] = weekly_average_players['week'].dt.to_timestamp()
        weekly_average_players = ['week', 'average_players', 'total_players']
        return weekly_average_players


    def insert_daily_total_players(self, daily_total_players):
        query = f"INSERT INTO {table名稱} (date, total_players) VALUES (%s, %s)"
        for index, row in daily_total_players.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['total_players']))

    def insert_weekly_average_players(self, weekly_average_players):
        query = f"INSERT INTO {table名稱} (week, average_players) VALUES (%s, %s)"
        for index, row in weekly_average_players.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['total_players']))

class DataAnalysis:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self, query):
        records = self.db_connection.execute_query(query)
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def analyze_data(self, df):
        df.set_index('timestamp', inplace=True)
        correlation, _ = pearsonr(df.index.astype(np.int64) // 10**9, df['value'])
        slope, intercept, r_value, p_value, std_err = linregress(df.index.astype(np.int64) // 10**9, df['value'])
        
        analysis_results = {
            'correlation': correlation,
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'p_value': p_value,
            'std_err': std_err
        }
        return df, analysis_results

    def distribution_test(self, df, dist_type='normal'):
        if dist_type == 'normal':
            dist = norm
        else:
            raise ValueError("Unsupported distribution type")

        params = dist.fit(df['value'])
        return params