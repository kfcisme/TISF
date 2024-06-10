import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest, uniform
import numpy as np
from db_connect import report_MySQLConnection
from fpdf import FPDF

class NewPlayerTrend(report_MySQLConnection):
    def __init__(self):
        super().__init__()

    def fetch_data(self):
        query = "SELECT timestamp, player_id FROM new_players"
        return self.execute_query(query)

    def weekly_new_players(self, records):
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.to_period('W')
        weekly_new_players = df.drop_duplicates(subset=['player_id']).groupby('timestamp').size().reset_index(name='new_players')
        weekly_new_players['timestamp'] = weekly_new_players['timestamp'].dt.to_timestamp()
        return weekly_new_players

    def ks_test(self, data):
        d_stat, p_value = kstest(data, 'uniform', args=(np.min(data), np.max(data) - np.min(data)))
        return d_stat, p_value

    def generate_trend_plot(self, weekly_new_players, plot_image_path):
        plt.figure(figsize=(12, 6))
        plt.plot(weekly_new_players['timestamp'], weekly_new_players['new_players'], label='每週新玩家', color='green')
        plt.title('每週新玩家趨勢')
        plt.xlabel('週')
        plt.ylabel('新玩家')
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, pdf_output_path, plot_image_path, ks_results):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="新玩家趨勢分析報告", ln=True, align='C')
        pdf.image(plot_image_path, x=10, y=20, w=190)
        pdf.ln(120)
        pdf.cell(200, 10, txt="Kolmogorov-Smirnov 檢驗結果:", ln=True)
        pdf.cell(200, 10, txt=f"D-統計值: {ks_results[0]:.4f}", ln=True)
        pdf.cell(200, 10, txt=f"P-值: {ks_results[1]:.4f}", ln=True)
        pdf.output(pdf_output_path)

    def insert_weekly_new_players(self, weekly_new_players):
        query = "INSERT INTO weekly_new_players (week, new_players) VALUES (%s, %s)"
        for index, row in weekly_new_players.iterrows():
            self.execute_insert(query, (row['timestamp'], row['new_players']))
