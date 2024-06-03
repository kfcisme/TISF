import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class server_RAM_mean:
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
