import discord
import json
from discord.ext import commands
import datetime

with open(file='c:\\Users\\arthu\\Downloads\\side project\\DiscordBot\\setup.json', mode='r', encoding='utf8') as file:
    data = json.load(file)

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
    pdf_path = 'c:\\Users\\arthu\\Downloads\\001.113年青少年科學人才培育計畫簡章v2.pdf'
    with open(pdf_path, 'rb') as pdf:
        discord_file = discord.File(pdf, filename="report.pdf")
        if data > '12' and data <= str(time.year):
            await ctx.send(f'已生成 {data} 年的年報表，資料庫名稱為 {database_name}', file=discord_file)
        elif data >= '1' and data <= str(time.month):
            await ctx.send(f'已生成 {data} 月的月報表，資料庫名稱為 {database_name}', file=discord_file)
        elif data > str(time.month):
            await ctx.send(f'已生成{time.year-1}年的{data}月月報表，資料庫名稱為 {database_name}', file=discord_file)
        else:
            await ctx.send(f'⚠️請輸入正確的西元年份或月份')
bot.run(data['TOKEN'])