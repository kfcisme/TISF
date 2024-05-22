import discord
from discord.ext import commands
import datetime
from config import DISCORD_TOKEN
from db_connection import MySQLConnection
from operation import DataAnalysis
from avgAFktime import ReportGenerator

class DiscordBot:
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.time = datetime.datetime.now()
        self.setup()

    def setup(self):
        @self.bot.event
        async def on_ready():
            print("The bot has successfully run!!!")

        @self.bot.command()
        async def reload(ctx): 
            await ctx.send('The bot has been reloaded!')

        @self.bot.command()
        async def report(ctx, database_name: str, data: str):
            try:
                db_conn = MySQLConnection()
                connection = db_conn.connect()
                
                analysis = DataAnalysis(connection)
                query = f"SELECT x, y FROM {database_name}" 
                df = analysis.fetch_data(query)
                analyzed_data, analysis_results = analysis.analyze_data(df)

                plot_image_path = "line_plot.png"
                pdf_output_path = "data_analysis_report.pdf"
                report = ReportGenerator(analyzed_data, analysis_results)
                report.generate_line_plot(plot_image_path)
                report.generate_pdf_report(pdf_output_path, plot_image_path)
                
                with open(pdf_output_path, 'rb') as pdf:
                    discord_file = discord.File(pdf, filename="report.pdf")
                    if int(data) > 12 and int(data) <= self.time.year:
                        await ctx.send(f'已生成 {data} 年的年報表，資料庫名稱為 {database_name}', file=discord_file)
                    elif int(data) >= 1 and int(data) <= self.time.month:
                        await ctx.send(f'已生成 {data} 月的月報表，資料庫名稱為 {database_name}', file=discord_file)
                    elif int(data) > self.time.month and int(data) <= 12:
                        await ctx.send(f'已生成{self.time.year-1}年的{data}月月報表，資料庫名稱為 {database_name}', file=discord_file)
                    else:
                        await ctx.send(f'⚠️請輸入正確的西元年份或月份')
            except Exception as e:
                await ctx.send(f'出現錯誤: {str(e)}')
            finally:
                db_conn.close()

    def run(self):
        self.bot.run(DISCORD_TOKEN)