import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from analysis import db_connect
from analysis import server_ram_and_TPS
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} 已連接到 Discord！")

@bot.command()
async def reload(ctx):
    await ctx.send('機器人正在重新加載配置和數據...')

@bot.command()
async def report(ctx, metric: str, period: str):
    if metric not in ['ram', 'tps']:
        await ctx.send('指定的指標無效。請使用 "ram" 或 "tps"。')
        return
    if period not in ['daily', 'weekly']:
        await ctx.send('指定的期間無效。請使用 "daily" 或 "weekly"。')
        return

    analysis_db_conn = db_connect.analysis_MySQLConnection()
    try:
        analysis_db_conn.connect()
        analyzer = server_ram_and_TPS.ServerAnalysis(analysis_db_conn, metric)
        data = analyzer.fetch_data()
        if period == 'daily':
            stats = analyzer.daily_statistics(data)
        else:
            stats = analyzer.weekly_statistics(data)

        result_message = f"{metric.upper()} {period} 統計資料：\n"
        for index, row in stats.iterrows():
            result_message += f"日期：{row['date']}, 平均值：{row['mean']:.2f}, 標準差：{row['std']:.2f}\n"
        
        await ctx.send(result_message)
    except Exception as error:
        await ctx.send(f'生成報告時出現錯誤：{str(error)}')
    finally:
        analysis_db_conn.close()

bot.run(DISCORD_TOKEN)