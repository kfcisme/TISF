import matplotlib.pyplot as plt
from fpdf import FPDF
from db_connect import report_MySQLConnection

class ServerRAMAnalysis(report_MySQLConnection):
    def __init__(self, analyzed_data, analysis_results):
        super().__init__()
        self.analyzed_data = analyzed_data
        self.analysis_results = analysis_results

    def generate_line_plot(self, plot_image_path):
        plt.figure(figsize=(10, 6))
        plt.plot(self.analyzed_data.index, self.analyzed_data['value'], label='TPS')
        plt.title('TPS時間序列')
        plt.xlabel('時間')
        plt.ylabel('使用量 (GB)')
        plt.legend()
        plt.savefig(plot_image_path)
        plt.close()

    def generate_pdf_report(self, dist_params, dist_type, plot_image_path, pdf_output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="TPS數據分析報告", ln=True, align='C')

        # 插入分析結果
        for key, value in self.analysis_results.items():
            pdf.cell(200, 10, txt=f"{key}: {value:.2f}", ln=True)

        # 插入分布參數
        pdf.cell(200, 10, txt=f"{dist_type.capitalize()} 分布參數: {dist_params}", ln=True)

        # 插入圖表
        pdf.image(plot_image_path, x=10, y=80, w=180)
        pdf.output(pdf_output_path)
