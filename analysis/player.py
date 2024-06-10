import pandas as pd
from db_connect import analysis_MySQLConnection
from scipy.stats import pearsonr, linregress
import numpy as np

class PlayerAnalysis(analysis_MySQLConnection):
    def fetch_data(self, query):
        """从数据库获取数据"""
        return self.execute_query(query)

    def compute_daily_and_weekly_stats(self, records):
        """计算每日和每周玩家统计"""
        df = pd.DataFrame(records, columns=['timestamp', 'player_name'])
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        

        daily_totals = df.drop_duplicates(['date', 'player_name']).groupby('date').size().reset_index(name='total_players')
        

        daily_totals['week'] = pd.to_datetime(daily_totals['date']).dt.to_period('W').dt.start_time
        weekly_averages = daily_totals.groupby('week')['total_players'].mean().reset_index()
        
        return daily_totals, weekly_averages

    def calculate_peak_hours(self, records):
        """计算每日的玩家高峰时间"""
        df = pd.DataFrame(records, columns=['timestamp', 'player_name'])
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['date'] = pd.to_datetime(df['timestamp']).dt.date


        hourly_counts = df.groupby(['date', 'hour']).size().reset_index(name='player_count')
        daily_peak = hourly_counts.loc[hourly_counts.groupby('date')['player_count'].idxmax()]

        return daily_peak

    def insert_statistics(self, data, table_name):
        for index, row in data.iterrows():
            query = f"INSERT INTO {table_name} (date, players) VALUES (%s, %s)"
            self.execute_insert(query, (row['date'], row['players']))

    def perform_analysis(self, df):
        df.set_index('date', inplace=True)
        correlation, _ = pearsonr(df.index.astype(np.int64), df['total_players'])
        regression = linregress(df.index.astype(np.int64), df['total_players'])
        
        return {
            'correlation': correlation,
            'slope': regression.slope,
            'intercept': regression.intercept,
            'r_value': regression.rvalue,
            'p_value': regression.pvalue,
            'std_err': regression.stderr
        }