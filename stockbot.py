
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
async def price(context,arg):
    print('got inside price')
    ticker_text = str(arg)
    print('Ticker Requested:' + ticker_text)
    try:
        ticker = yf.Ticker(ticker_text)
        ticker_info = ticker.info
        print('Info received on ' + ticker_text)
        if(str(ticker_info['regularMarketPrice']) == 'None'):
            raise Exception("INVALID_TICKER_ERROR")
        else:
            price = str(ticker_info['regularMarketPrice'])
    except Exception as e:
        await context.send(content=e)
        return
    await context.send(content=getPriceOutput(ticker_text,ticker_info['shortName'],price,ticker_info['open']))

bot.run(DISCORD_TOKEN)