import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class world_ram_mean:
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

    def monthly_average(self, daily_average):
        daily_average['month'] = daily_average['timestamp'].dt.to_period('M')
        monthly_average = daily_average.groupby('month')['value'].mean().reset_index()
        monthly_average['month'] = monthly_average['month'].dt.to_timestamp()
        return monthly_average

    def insert_daily_average(self, daily_average):
        query = f"INSERT INTO {table名稱} (date, average) VALUES (%s, %s)"
        for index, row in daily_average.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['value']))

    def insert_monthly_average(self, monthly_average):
        query = f"INSERT INTO {table名稱} (month, average) VALUES (%s, %s)"
        for index, row in monthly_average.iterrows():
            self.db_connection.execute_insert(query, (row['month'], row['value']))
