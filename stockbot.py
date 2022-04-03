
import os
import traceback
from decimal import Decimal

import nextcord
import yfinance as yf
from dotenv import load_dotenv
from nextcord.ext import commands

from portfolio_add import *
from portfolio_show import *
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
        if(await isValidTicker(ticker_name,context)):
            await context.send(embed=getPriceOutput(ticker_stats,args[1:len(args)]))

    #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
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
            if(not(await isValidTicker(ticker,context))):
                return
                
            #add to the user's portfolio and returns the return message
            return_message = portfolio_add(user_id, ticker,avg_price,share_amt)
            await context.send(content=return_message)
        if(command == 'show'):
            print(str(args))
            print(context.message.mentions)
            try:
                user:str = str(context.message.mentions[0].id)
                user_name:str = context.message.mentions[0].display_name
            except IndexError as e:
                print(e)
                print("No user specified, defaulting to sender")
                user:str = str(context.author.id)
                user_name:str = (await bot.fetch_user(user)).display_name
            await context.send(embed = portfolio_show(user,user_name))
    #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return
    
bot.run(DISCORD_TOKEN)
