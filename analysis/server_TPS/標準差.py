import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection
#浮點數
class server_TPS_Std:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, value FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def daily_server_TPS_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_stats = df.resample('D', on='timestamp').agg(['mean', 'std']).reset_index()
        daily_stats.columns = ['timestamp', 'mean', 'std']
        return daily_stats

    def monthly_server_TPS_std(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month'] = df['timestamp'].dt.to_period('M')
        monthly_std = df.groupby('month')['value'].std().reset_index()
        monthly_std['month'] = monthly_std['month'].dt.to_timestamp()
        return monthly_std

    def insert_monthly_server_TPS_std(self, monthly_std):
        query = f"INSERT INTO {table名稱} (month, std_dev) VALUES (%s, %s)"
        for index, row in monthly_std.iterrows():
            self.db_connection.execute_insert(query, (row['month'], row['value']))
