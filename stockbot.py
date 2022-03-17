
import os
import nextcord
from nextcord.ext import commands
import yfinance as yf
import re
from dotenv import load_dotenv

from yfincode import getPriceOutput

#loads dotenv for KEYS
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot=commands.Bot(command_prefix='!stockbot ')

@bot.event
async def on_ready():
    print('Logged on !')

@bot.command()
async def price(context,ticker_name):
    print('Ticker Requested:' + ticker_name)
    try:
        ticker = yf.Ticker(ticker_name)
        print('Info received on ' + ticker_name)
        if (str(ticker.info['regularMarketPrice']) == 'None'):
            raise Exception("INVALID_TICKER_ERROR")
        else:
            await context.send(getPriceOutput(ticker.info))
    except Exception as e:
        await context.send(content=e)
        return

bot.run(DISCORD_TOKEN)