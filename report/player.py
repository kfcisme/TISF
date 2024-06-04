import matplotlib.pyplot as plt
from fpdf import FPDF

class player:
    def __init__(self):
        pass

    def line_plot(self, df, plot_image_path):
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['value'], label='Value')
        plt.title('Time Series Data')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(plot_image_path)
        plt.close()

    def pdf_report(self, analysis_results, dist_params, plot_image_path, pdf_output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')

        for key, value in analysis_results.items():
            pdf.cell(200, 10, txt=f"{key}: {value:.2f}", ln=True)

        pdf.cell(200, 10, txt=f"Normal Distribution Parameters: {dist_params}", ln=True)
        pdf.image(plot_image_path, x=10, y=100, w=180)
        pdf.output(pdf_output_path)

    def player_stats_report(self, daily_total_players, weekly_avg_total_players, plot_image_path, pdf_output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Player Statistics Report", ln=True, align='C')
        pdf.cell(200, 10, txt="Daily Total Players:", ln=True)

        for index, row in daily_total_players.iterrows():
            pdf.cell(200, 10, txt=f"{row['timestamp']}: {row['total_players']}", ln=True)

        pdf.cell(200, 10, txt="Weekly Average Players:", ln=True)

        for index, row in weekly_avg_total_players.iterrows():
            pdf.cell(200, 10, txt=f"{row['week']}: {row['total_players']}", ln=True)
        
        pdf.image(plot_image_path, x=10, y=100, w=180)
        pdf.output(pdf_output_path)

    def peak_hour_report(self, peak_hours, plot_image_path, pdf_output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Player Peak Hour Report", ln=True, align='C')

        for index, row in peak_hours.iterrows():
            pdf.cell(200, 10, txt=f"{row['day']} {row['hour']}:00: {row['players']} players", ln=True)
        
        pdf.image(plot_image_path, x=10, y=100, w=180)
        pdf.output(pdf_output_path)