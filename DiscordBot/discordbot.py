import discord
import json
from discord.ext import commands
from cog import command
with open(file='setup.json', mode='r' , encoding='utf8') as file:
    data = json.load(file)

intents = discord.Intents.all()
intents.message_content = True
bot=commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
    print("the bot has successfully run!!!")

@bot.command()
async def reload(ctx): 
    await ctx.send(f'The bot has been reload!')

@bot.command()
async def report(ctx,database_name: str , data: str):   
    if data>'12':
        await ctx.send(f'已生成 {data} 年的年報表，資料庫名稱為 {database_name}')
    #get the report form PDF_generator
    else:
        await ctx.send(f'已生成 {data} 月的月報表，資料庫名稱為 {database_name}')
bot.run(data['TOKEN'])
#bot.run('MTIxNzI2MDk5OTM2Mzc5MzAzOA.GFICRg.1IeKg7zlt_VQWJAoKewlvrMkdthq9Wws8dbgDQ')