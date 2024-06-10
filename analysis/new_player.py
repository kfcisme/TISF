import pandas as pd
from scipy.stats import kstest, uniform
from db_connect import analysis_MySQLConnection  
import numpy as np

class NewPlayerTrend(analysis_MySQLConnection):
    def __init__(self):
        super().__init__()  

    def fetch_data(self):
        query = "SELECT date, player_name FROM registration"
        return self.execute_query(query)  

    def weekly_new_players(self, records):
        df = pd.DataFrame(records, columns=['date', 'player_name'])
        df['date'] = pd.to_datetime(df['date']).dt.to_period('W')
        weekly_new_players = df.drop_duplicates(subset=['player_name']).groupby('date').size().reset_index(name='new_players')
        weekly_new_players['date'] = weekly_new_players['date'].dt.to_timestamp()
        return weekly_new_players

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def insert_weekly_new_players(self, weekly_new_players):
        query = "INSERT INTO weekly_new_players (week, new_players) VALUES (%s, %s)"
        for index, row in weekly_new_players.iterrows():
            self.execute_insert(query, (row['date'], row['new_players']))


#if __name__ == "__main__":
#    np_trend = NewPlayerTrend()
#    data = np_trend.fetch_data()
#    weekly_data = np_trend.weekly_new_players(data)
#    print(weekly_data)
#    np_trend.insert_weekly_new_players(weekly_data)