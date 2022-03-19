
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

bot=commands.Bot(command_prefix='!stock ')

@bot.event
async def on_ready():
    print('Logged on !')

@bot.command()
async def price(context,ticker_name):
    print('Ticker Requested:' + ticker_name)
    try:
        ticker = yf.Ticker(ticker_name)

        ticker_stats = ticker.stats()
        print('Info received on ' + ticker_name)

        #try accesing the market price, returns KeyError if there is none
        try:
            ticker_stats['price']['regularMarketPrice']
        except KeyError as e:
            #tell user they entered the wrong ticker
            print("Exception:" + str(e))
            await context.send(content='Invalid Ticker, please try again')
            return
        #pass ticker_stats to get the output
        await context.send(getPriceOutput(ticker_stats))

    #print unknown exeception for all other exceptions
    except Exception as e:
        print("Exception:" + str(e))
        await context.send(content='Unknown Exception Occured, please try again')
        return

bot.run(DISCORD_TOKEN)