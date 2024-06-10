import discord
from discord.ext import commands
from config import DISCORD_TOKEN
import datetime
import db_connect  # 確保此導入路徑正確
import server_ram
import server_TPS
import player
import block_update
import newplayer  # 假設您已有此分析類別

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} 已連接到 Discord！")

@bot.command()
async def reload(ctx):
    await ctx.send('機器人正在重新加載配置和數據...')

@bot.command()
async def report(ctx, analysis_type: str, period: str):
    if analysis_type not in ['ram', 'tps', 'player', 'block', 'newplayer']:
        await ctx.send('指定的分析類型無效。請使用 "ram", "tps", "player", "block", 或 "newplayer"。')
        return
    if period not in ['daily', 'weekly']:
        await ctx.send('指定的期間無效。請使用 "daily" 或 "weekly"。')
        return

    analysis_db_conn = db_connect.report_MySQLConnection()
    analysis_db_conn.connect()
    try:
        if analysis_type == 'ram':
            analyzer = server_ram.ServerRAMAnalysis(analysis_db_conn)
        elif analysis_type == 'tps':
            analyzer = server_TPS.ServerTPSAnalysis(analysis_db_conn)
        else:
            analyzer = getattr(globals()[analysis_type], f"{analysis_type.capitalize()}Analysis")(analysis_db_conn)
        
        data = analyzer.fetch_data()
        stats = analyzer.daily_statistics(data) if period == 'daily' else analyzer.weekly_statistics(data)

        result_message = f"{analysis_type.upper()} {period} 統計資料：\n"
        for index, row in stats.iterrows():
            result_message += f"日期：{row['date']}, 平均值：{row['mean']:.2f}, 標準差：{row['std']:.2f}\n"
        
        await ctx.send(result_message)
    except Exception as error:
        await ctx.send(f'生成報告時出現錯誤：{str(error)}')
    finally:
        analysis_db_conn.close()

bot.run(DISCORD_TOKEN)
