import pandas as pd
from datetime import datetime
from scipy.stats import kstest, uniform
import numpy as np
from db_connection import MySQLConnection

class NewPlayerTrend:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = "SELECT timestamp, player_id FROM new_players"
        records = self.db_connection.execute_query(query)
        return records

    def weekly_new_players(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.to_period('W')
        weekly_new_players = df.drop_duplicates(subset=['player_id']).groupby('timestamp').size().reset_index(name='new_players')
        weekly_new_players['timestamp'] = weekly_new_players['timestamp'].dt.to_timestamp()
        return weekly_new_players

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def insert_weekly_new_players(self, weekly_new_players):
        query = "INSERT INTO weekly_new_players (week, new_players) VALUES (%s, %s)"
        for index, row in weekly_new_players.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['new_players']))