import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import kstest, uniform
import numpy as np
from db_connection import MySQLConnection
from fpdf import FPDF

class BlockUpdateTrend:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self):
        query = "SELECT timestamp, update_id FROM block_updates"
        records = self.db_connection.execute_query(query)
        return records

    def daily_statistics(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'update_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('timestamp')['update_id'].count().reset_index(name='total_updates')
        daily_stats = daily_counts.agg(['mean', 'std', 'sum']).transpose().reset_index()
        daily_stats.columns = ['date', 'mean_updates', 'std_updates', 'total_updates']
        return daily_counts, daily_stats

    def week_statistics(self, daily_counts):
        daily_counts['week'] = pd.to_datetime(daily_counts['timestamp']).dt.to_period('W')
        weekly_stats = daily_counts.groupby('week')['total_updates'].agg(['mean', 'std', 'sum']).reset_index()
        weekly_stats.columns = ['week', 'mean_updates', 'std_updates', 'total_updates']
        weekly_stats['week'] = weekly_stats['week'].dt.to_timestamp()
        return weekly_stats

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def generate_trend_plot(self, daily_counts, weekly_stats, plot_image_path):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(daily_counts['timestamp'], daily_counts['total_updates'], label='Daily Updates')
        plt.title('Daily Updates Trend')
        plt.xlabel('Date')
        plt.ylabel('Total Updates')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(weekly_stats['week'], weekly_stats['total_updates'], label='Weekly Updates', color='orange')
        plt.title('Weekly Updates Trend')
        plt.xlabel('Week')
        plt.ylabel('Total Updates')
        plt.legend()

        plt.tight_layout()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, pdf_output_path, plot_image_path, ks_results):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="方塊更新變化趨勢", ln=True, align='C')

        pdf.image(plot_image_path, x=10, y=20, w=190)

        pdf.ln(120)
        pdf.cell(200, 10, txt=f"Kolmogorov-Smirnov Test Results:", ln=True)
        pdf.cell(200, 10, txt=f"D-statistic: {ks_results[0]:.4f}", ln=True)
        pdf.cell(200, 10, txt=f"P-value: {ks_results[1]:.4f}", ln=True)

        pdf.output(pdf_output_path)

    def insert_daily_statistics(self, daily_counts):
        query = "INSERT INTO daily_update_stats (date, total_updates) VALUES (%s, %s)"
        for index, row in daily_counts.iterrows():
            self.db_connection.execute_insert(query, (row['timestamp'], row['total_updates']))

    def insert_weekly_statistics(self, weekly_stats):
        query = "INSERT INTO weekly_update_stats (week, mean_updates, std_updates, total_updates) VALUES (%s, %s, %s, %s)"
        for index, row in weekly_stats.iterrows():
            self.db_connection.execute_insert(query, (row['week'], row['mean_updates'], row['std_updates'], row['total_updates']))
