import matplotlib.pyplot as plt
from fpdf import FPDF

class server_ram_report:
    def __init__(self, analyzed_data, analysis_results):
        self.analyzed_data = analyzed_data
        self.analysis_results = analysis_results

    def generate_line_plot(self, plot_image_path):
        plt.figure(figsize=(10, 6))
        plt.plot(self.analyzed_data.index, self.analyzed_data['value'], label='Value')
        plt.title('Time Series Data')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, dist_params, dist_type, plot_image_path, pdf_output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')
        for key, value in self.analysis_results.items():
            pdf.cell(200, 10, txt=f"{key}: {value:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"{dist_type.capitalize()} Distribution Parameters: {dist_params}", ln=True)
        
        pdf.image(plot_image_path, x=10, y=100, w=180)
        pdf.output(pdf_output_path)