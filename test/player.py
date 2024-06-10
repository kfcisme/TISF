import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from db_connect import report_MySQLConnection

class PlayerAnalysis(report_MySQLConnection):
    def __init__(self):
        super().__init__()

    def fetch_data(self, query):
        """從數據庫提取數據"""
        return self.execute_query(query)

    def process_player_stats(self, records):
        """處理玩家統計數據，計算每日和每週總玩家數"""
        df = pd.DataFrame(records, columns=['timestamp', 'player_id'])
        df['date'] = pd.to_datetime(df['timestamp']).dt.date

        # 每日玩家統計
        daily_total = df.drop_duplicates(subset=['date', 'player_id']).groupby('date').size().reset_index(name='total_players')
        daily_total['week'] = pd.to_datetime(daily_total['date']).dt.to_period('W').dt.start_time

        # 每週平均玩家數
        weekly_avg = daily_total.groupby('week')['total_players'].mean().reset_index()

        return daily_total, weekly_avg

    def generate_plots(self, daily_data, weekly_data, plot_image_path):
        """生成每日和每週玩家數據的圖表"""
        plt.figure(figsize=(10, 6))
        plt.plot(daily_data['date'], daily_data['total_players'], label='每日玩家數')
        plt.plot(weekly_data['week'], weekly_data['total_players'], label='每週平均玩家數', linestyle='--')
        plt.title('玩家活動趨勢')
        plt.xlabel('日期')
        plt.ylabel('玩家數量')
        plt.legend()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, plot_image_path, daily_data, weekly_data, pdf_output_path):
        """生成包含玩家數據的 PDF 報告"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="玩家統計報告", ln=True, align='C')

        pdf.image(plot_image_path, x=10, y=30, w=180)
        pdf.ln(100)  # 移動到圖表下方

        pdf.cell(200, 10, txt="每日玩家統計:", ln=True)
        for index, row in daily_data.iterrows():
            pdf.cell(200, 10, txt=f"{row['date']}: {row['total_players']}玩家", ln=True)

        pdf.cell(200, 10, txt="每週平均玩家統計:", ln=True)
        for index, row in weekly_data.iterrows():
            pdf.cell(200, 10, txt=f"{row['week']}: {row['total_players']:.2f}玩家", ln=True)

        pdf.output(pdf_output_path)
