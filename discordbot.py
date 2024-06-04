import discord
from cog import command
from discord.ext import commands
import datetime
from db_connection import MySQLConnection
from report import *
from analysis import *
from config import DISCORD_TOKEN
from config import DB_NAME
#class DiscordBot:
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print("The bot has successfully run!!!")

@bot.command()
async def reload(ctx): 
        await ctx.send('The bot has been reloaded!')

@bot.command()
async def report(ctx, database_name: str, data: str):
    time = datetime.datetime.now()
    try:
        db_conn = MySQLConnection()
        connection = db_conn.connect()
            
        analysis = analysis(connection)
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
            if int(data) > 12 and int(data) <= time.year:
                await ctx.send(f'已生成 {data} 年的年報表，資料庫名稱為 {database_name}', file=discord_file)
            elif int(data) >= 1 and int(data) <= time.week:
                await ctx.send(f'已生成 {data} 月的月報表，資料庫名稱為 {database_name}', file=discord_file)
            elif int(data) > time.week and int(data) <= 12:
                await ctx.send(f'已生成{time.year-1}年的{data}月月報表，資料庫名稱為 {database_name}', file=discord_file)
            else:
                await ctx.send(f'⚠️請輸入正確的西元年份或月份')
    except Exception as error:
        await ctx.send(f'出現錯誤: {str(error)}')
    finally:
            db_conn.close()
bot.run(DISCORD_TOKEN)