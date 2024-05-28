import pandas as pd
from datetime import datetime
from db_connection import MySQLConnection

class player_peak_hour:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = f"SELECT timestamp, players FROM {table名稱}"
        records = self.db_connection.execute_query(query)
        return records

    def peak_hours(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'players'])
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day_name()
        peak_hours = df.groupby(['day', 'hour'])['players'].max().reset_index()
        return peak_hours

    def insert_peak_hours(self, peak_hours):
        query = f"INSERT INTO {table名稱} (day, hour, max_players) VALUES (%s, %s, %s)"
        for index, row in peak_hours.iterrows():
            self.db_connection.execute_insert(query, (row['day'], row['hour'], row['players']))
