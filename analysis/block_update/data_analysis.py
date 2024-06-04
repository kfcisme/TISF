import pandas as pd
from datetime import datetime
from scipy.stats import kstest, ks_2samp, uniform
import numpy as np
from db_connection import MySQLConnection

class blockupdatetrend:
    def __init__(self, connection):
        self.db_connection = connection

    def fetch_data(self):
        query = "SELECT timestamp, update_id FROM block_updates"
        records = self.db_connection.execute_query(query)
        return records

    def daily_statistics(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'update_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('timestamp')['update_id'].count().reset_index(name='total_updates')
        daily_stats = daily_counts.agg(['mean', 'std', 'sum']).transpose().reset_index()
        daily_stats.columns = ['date', 'mean_updates', 'std_updates', 'total_updates']
        return daily_counts, daily_stats

    def week_statistics(self, daily_counts):
        daily_counts['week'] = pd.to_datetime(daily_counts['timestamp']).dt.to_period('W')
        weekly_stats = daily_counts.groupby('week')['total_updates'].agg(['mean', 'std', 'sum']).reset_index()
        weekly_stats.columns = ['week', 'mean_updates', 'std_updates', 'total_updates']
        weekly_stats['week'] = weekly_stats['week'].dt.to_timestamp()
        return weekly_stats

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def insert_daily_statistics(self, daily_counts):
        query = "INSERT INTO daily_update_stats (date, total_updates) VALUES (%s, %s)"
        for index, row in daily_counts.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['total_updates']))

    def insert_weekly_statistics(self, weekly_stats):
        query = "INSERT INTO weekly_update_stats (week, mean_updates, std_updates, total_updates) VALUES (%s, %s, %s, %s)"
        for index, row in weekly_stats.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['mean_updates'], row['std_updates'], row['total_updates']))