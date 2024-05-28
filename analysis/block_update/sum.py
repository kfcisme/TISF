import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class block_update:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, update_id FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_statistics(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'update_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('timestamp')['update_id'].count().reset_index(name='total_updates')
        daily_stats = daily_counts.agg(['mean', 'std', 'sum']).transpose().reset_index()
        daily_stats.columns = ['date', 'mean_updates', 'std_updates', 'total_updates']
        return daily_counts, daily_stats

    def calculate_monthly_statistics(self, daily_counts):
        daily_counts['month'] = pd.to_datetime(daily_counts['timestamp']).dt.to_period('M')
        monthly_stats = daily_counts.groupby('month')['total_updates'].agg(['mean', 'std', 'sum']).reset_index()
        monthly_stats.columns = ['month', 'mean_updates', 'std_updates', 'total_updates']
        monthly_stats['month'] = monthly_stats['month'].dt.to_timestamp()
        return monthly_stats

    def insert_daily_statistics(self, daily_counts):
        query = f"INSERT INTO {table名稱} (date, total_updates) VALUES (%s, %s)"
        for index, row in daily_counts.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['total_updates']))

    def insert_monthly_statistics(self, monthly_stats):
        query = f"INSERT INTO {table名稱} (month, mean_updates, std_updates, total_updates) VALUES (%s, %s, %s, %s)"
        for index, row in monthly_stats.iterrows():
            self.db_connection.execute_insert(query, (row['month'], row['mean_updates'], row['std_updates'], row['total_updates']))
