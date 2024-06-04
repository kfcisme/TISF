import os
from fpdf import FPDF
import matplotlib.pyplot as plt

class ConsolidatedReport:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

    def generate_line_plot(self, data, plot_image_path):
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['value'], label='Value')
        plt.title('Time Series Data')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, title, analysis_results, dist_params, plot_image_path, pdf_output_path):
        self.pdf.cell(200, 10, txt=title, ln=True, align='C')
        for key, value in analysis_results.items():
            self.pdf.cell(200, 10, txt=f"{key}: {value:.2f}", ln=True)
        self.pdf.cell(200, 10, txt=f"Distribution Parameters: {dist_params}", ln=True)
        self.pdf.image(plot_image_path, x=10, y=self.pdf.get_y() + 10, w=180)
        self.pdf.output(pdf_output_path)

    def generate_player_stats_report(self, title, daily_total_players, weekly_avg_total_players, plot_image_path, pdf_output_path):
        self.pdf.cell(200, 10, txt=title, ln=True, align='C')
        self.pdf.cell(200, 10, txt="Daily Total Players:", ln=True)

        for index, row in daily_total_players.iterrows():
            self.pdf.cell(200, 10, txt=f"{row['timestamp']}: {row['total_players']}", ln=True)

        self.pdf.cell(200, 10, txt="Weekly Average Players:", ln=True)

        for index, row in weekly_avg_total_players.iterrows():
            self.pdf.cell(200, 10, txt=f"{row['week']}: {row['total_players']}", ln=True)

        self.pdf.image(plot_image_path, x=10, y=self.pdf.get_y() + 10, w=180)
        self.pdf.output(pdf_output_path)

    def generate_peak_hour_report(self, title, peak_hours, plot_image_path, pdf_output_path):
        self.pdf.cell(200, 10, txt=title, ln=True, align='C')

        for index, row in peak_hours.iterrows():
            self.pdf.cell(200, 10, txt=f"{row['day']} {row['hour']}:00: {row['players']} players", ln=True)

        self.pdf.image(plot_image_path, x=10, y=self.pdf.get_y() + 10, w=180)
        self.pdf.output(pdf_output_path)
        def consolidate_reports(report_files, output_pdf_path):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            for file_path in report_files:

                if file_path.endswith('.pdf'):
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)

                    with open(file_path, 'rb') as file:
                        pdf_data = file.read()
                        pdf.add_page()
                        pdf.image(file_path, x=10, y=10, w=190)
                        
                elif file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=os.path.basename(file_path), ln=True, align='C')
                    pdf.image(file_path, x=10, y=20, w=190)
            
            pdf.output(output_pdf_path)