
import os
from decimal import Decimal

import nextcord
import yfinance as yf
from dotenv import load_dotenv
from nextcord.ext import commands

from portfolio import *
from yfincode import *

#loads dotenv for KEYS
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot=commands.Bot(command_prefix='!stock ')

@bot.event
async def on_ready():
    print('Logged on !')

@bot.command()
async def price(context,*args):
    ticker_name:str = args[0]
    print('Ticker Requested:' + ticker_name)
    try:
        ticker = yf.Ticker(ticker_name)

        ticker_stats:dict = ticker.stats()
        print('Info received on ' + ticker_name)

        #returns data if the ticker is valid
        if(isValidTicker(ticker_name,context)):
            await context.send(embed=getPriceOutput(ticker_stats,args[1:len(args)]))

    #print unknown exeception for all other exceptions
    except Exception as e:
        print("Exception:" + str(e))
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return

@bot.command()
async def portfolio(context,*args):
    try:
        #retreive user id and command
        user_id:str = str(context.author.id) 
        command:str = args[0]
        if(command == 'add'):
            #retreive variables from args
            ticker:str = args[1]
            avg_price:Decimal = Decimal(args[2])
            share_amt:int = int(args[3])

            #check for valid ticker
            if(not(isValidTicker(ticker,context))):
                return
                
            #add to the user's portfolio and returns the return message
            return_message = portfolio_add(user_id, ticker,avg_price,share_amt)
            await context.send(content=return_message)

    #print unknown exeception for all other exceptions
    except Exception as e:
        print("Exception:" + str(e))
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return
    
bot.run(DISCORD_TOKEN)
