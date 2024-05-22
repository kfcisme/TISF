import matplotlib.pyplot as plt
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data, analysis_results):
        self.data = data
        self.analysis_results = analysis_results

    def generate_line_plot(self, output_path):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['x'], self.data['y'], marker='o', label='Data')
        plt.plot(self.data['x'], self.data['regression_line'], color='red', label='Regression Line')
        plt.title('Line Plot with Regression Line')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()

    def generate_pdf_report(self, pdf_output_path, plot_image_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')
        pdf.ln(10)
        
        pdf.cell(200, 10, txt=f"Mean: {self.analysis_results['mean'].to_dict()}", ln=True)
        pdf.cell(200, 10, txt=f"Standard Deviation: {self.analysis_results['std'].to_dict()}", ln=True)
        pdf.cell(200, 10, txt=f"Regression Slope: {self.analysis_results['slope']}", ln=True)
        pdf.cell(200, 10, txt=f"Regression Intercept: {self.analysis_results['intercept']}", ln=True)
        pdf.cell(200, 10, txt=f"R-squared: {self.analysis_results['r_value']**2}", ln=True)
        pdf.cell(200, 10, txt=f"P-value: {self.analysis_results['p_value']}", ln=True)
        pdf.cell(200, 10, txt=f"Standard Error: {self.analysis_results['std_err']}", ln=True)
        
        pdf.ln(10)
        
        # 圖像
        pdf.image(plot_image_path, x=10, y=None, w=190)
        
        pdf.output(pdf_output_path)


