import pandas as pd
from scipy.stats import kstest, norm
from db_connect import analysis_MySQLConnection
import numpy as np

class BlockUpdateAnalysis(analysis_MySQLConnection):
    def fetch_data(self):
        query = "SELECT date, block FROM block_break"
        return self.execute_query(query)

    def daily_statistics(self, records):
        df = pd.DataFrame(records, columns=['date', 'block'])
        df['date'] = pd.to_datetime(df['date']).dt.date
        daily_counts = df.groupby('date')['block'].count().reset_index(name='total_updates')
        return daily_counts

    def weekly_statistics(self, daily_counts):
        daily_counts['week'] = pd.to_datetime(daily_counts['date']).dt.to_period('W')
        weekly_stats = daily_counts.groupby('week')['total_updates'].agg(['mean', 'std', 'sum']).reset_index()
        return weekly_stats

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'norm', args=(np.mean(data), np.std(data)))
        return d_stat, p_value

    def insert_daily_statistics(self, daily_counts):
        query = "INSERT INTO daily_update_stats (date, total_updates) VALUES (%s, %s)"
        for index, row in daily_counts.iterrows():
            self.execute_insert(query, (row['date'], row['total_updates']))

    def insert_weekly_statistics(self, weekly_stats):
        query = "INSERT INTO weekly_update_stats (week, mean_updates, std_updates, total_updates) VALUES (%s, %s, %s, %s)"
        for index, row in weekly_stats.iterrows():
            self.execute_insert(query, (row['week'], row['mean_updates'], row['std_updates'], row['total_updates']))