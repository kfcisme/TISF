import pandas as pd
from datetime import datetime
import numpy as np
from scipy.stats import pearsonr, linregress, norm, uniform
from db_connect import analysis_MySQLConnection

class ServerAnalysis(analysis_MySQLConnection):
    def __init__(self, db_connection, metric):
        super().__init__()
        self.db_connection = db_connection
        self.metric = metric  # 'ram' 或 'tps'

    def fetch_data(self):
        table = 'ram' if self.metric == 'ram' else 'tps'
        query = f"SELECT date, value FROM {table}"
        return self.execute_query(query)

    def daily_statistics(self, records):
        df = pd.DataFrame(records, columns=['date', 'value'])
        df['date'] = pd.to_datetime(df['date'])
        daily_stats = df.resample('D', on='date').agg(['mean', 'std']).reset_index()
        daily_stats.columns = ['date', 'mean', 'std']
        return daily_stats

    def weekly_statistics(self, daily_stats):
        daily_stats['week'] = daily_stats['date'].dt.to_period('M')
        weekly_stats = daily_stats.groupby('week')['value'].agg(['mean', 'std']).reset_index()
        weekly_stats['week'] = weekly_stats['week'].dt.to_timestamp()
        return weekly_stats

    def insert_statistics(self, stats, period='daily'):
        table = f"{self.metric}_{period}_stats"
        stats_type = 'std_dev' if period == 'weekly' else 'average'
        for index, row in stats.iterrows():
            query = f"INSERT INTO {table} (date, {stats_type}) VALUES (%s, %s)"
            self.execute_insert(query, (row['date'], row[stats_type]))

    def analyze_data(self, df):
        df.set_index('date', inplace=True)
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
        return analysis_results

    def distribution_test(self, df, dist_type='normal'):
        if dist_type == 'normal':
            dist = norm
        elif dist_type == 'uniform':
            dist = uniform
        else:
            raise ValueError("Unsupported distribution type")
        params = dist.fit(df['value'])
        return params