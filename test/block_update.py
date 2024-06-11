import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest, uniform
import numpy as np
from db_connect import report_MySQLConnection
from fpdf import FPDF

class BlockUpdateAnalysis(report_MySQLConnection):
    def __init__(self):
        super().__init__()

    def fetch_data(self):

        query = "SELECT timestamp, update_id FROM block_updates"
        return self.execute_query(query)

    def daily_statistics(self, records):

        df = pd.DataFrame(records, columns=['timestamp', 'update_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby('timestamp')['update_id'].count().reset_index(name='total_updates')
        return daily_counts

    def weekly_statistics(self, daily_counts):

        daily_counts['week'] = pd.to_datetime(daily_counts['timestamp']).dt.to_period('W').dt.start_time
        weekly_stats = daily_counts.groupby('week')['total_updates'].agg(['mean', 'std', 'sum']).reset_index()
        weekly_stats.columns = ['week', 'mean_updates', 'std_updates', 'total_updates']
        return weekly_stats

    def ks_test(self, data):

        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def generate_trend_plot(self, daily_counts, weekly_stats, plot_image_path):

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(daily_counts['timestamp'], daily_counts['total_updates'], label='每日更新')
        plt.title('每日更新趨勢')
        plt.xlabel('日期')
        plt.ylabel('更新總數')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(weekly_stats['week'], weekly_stats['total_updates'], label='每週更新', color='orange')
        plt.title('每週更新趨勢')
        plt.xlabel('週')
        plt.ylabel('更新總數')
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, pdf_output_path, plot_image_path, ks_results):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="方塊更新變化趨勢報告", ln=True, align='C')
        pdf.image(plot_image_path, x=10, y=30, w=190)
        pdf.ln(105)  # 移動到下方

        pdf.cell(200, 10, txt="Kolmogorov-Smirnov 檢驗結果:", ln=True)
        pdf.cell(200, 10, txt=f"D-統計值: {ks_results[0]:.4f}, P-值: {ks_results[1]:.4f}", ln=True)
        pdf.output(pdf_output_path)
