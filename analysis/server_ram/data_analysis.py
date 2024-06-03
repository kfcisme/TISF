import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection
import numpy as np
from scipy.stats import pearsonr, linregress, norm, uniform
class Std:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, value FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_server_ram_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_stats = df.resample('D', on='timestamp').agg(['mean', 'std']).reset_index()
        daily_stats.columns = ['timestamp', 'mean', 'std']
        return daily_stats

    def weekly_server_ram_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['week'] = df['timestamp'].dt.to_period('M')
        weekly_std = df.groupby('week')['value'].std().reset_index()
        weekly_std['week'] = weekly_std['week'].dt.to_timestamp()
        return weekly_std

    def insert_weekly_server_ram_std(self, weekly_std):
        query = f"INSERT INTO {table名稱} (week, std_dev) VALUES (%s, %s)"
        for index, row in weekly_std.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['value']))

class mean:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, value FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_average(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_average = df.resample('D', on='timestamp').mean().reset_index()
        return daily_average

    def weekly_average(self, daily_average):
        daily_average['week'] = daily_average['timestamp'].dt.to_period('M')
        weekly_average = daily_average.groupby('week')['value'].mean().reset_index()
        weekly_average['week'] = weekly_average['week'].dt.to_timestamp()
        return weekly_average

    def insert_daily_average(self, daily_average):
        query = f"INSERT INTO {table名稱} (date, average) VALUES (%s, %s)"
        for index, row in daily_average.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['value']))

    def insert_weekly_average(self, weekly_average):
        query = f"INSERT INTO {table名稱} (week, average) VALUES (%s, %s)"
        for index, row in weekly_average.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['value']))

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
        correlation, _ = pearsonr(df.index.astype(np.int64), df['value'])
        slope, intercept, r_value, p_value, std_err = linregress(df.index.astype(np.int64), df['value'])
        
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
        elif dist_type == 'uniform':
            dist = uniform
        else:
            raise ValueError("Unsupported distribution type")

        params = dist.fit(df['value'])
        return params