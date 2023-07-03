#main bot function

import os
import traceback
from decimal import Decimal
from argparse import ArgumentParser

import nextcord
import yfinance as yf
from dotenv import load_dotenv
from nextcord.ext import commands
from portfolio import portfolio_add, portfolio_show, parsePortfolioArgs
from portfolioSQLiteDB import positionBelongsToUser, removePosition

from yfincode import *

#loads dotenv for KEYS
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = nextcord.Intents.default()
intents.message_content = True
bot=commands.Bot(command_prefix='!stock ',intents=intents)

@bot.event
async def on_ready():
    print('Logged on !')

@bot.command()
async def price(context,*args):
    parser = ArgumentParser()
    parser.add_argument('ticker',type=str)
    parser.add_argument('-r','--range',action='store_true')

    try:
        parsedArgs = parser.parse_args(args)
    except SystemExit as exit:
        await context.send(content='Invalid Arguments Provided')
        return

    print(parsedArgs)

    print("asked for price")
    tickerName:str = parsedArgs.ticker
    print('Ticker Requested:' + tickerName)
    try:
        #returns data if the ticker is valid
        if(await isValidTicker(tickerName)):
            await context.send(embed=getPriceOutput(parsedArgs))
        else:
            await context.send(content="Invalid Ticker Provided")

    #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return

@bot.command()
async def portfolio(context,*args):
    try:
        print(args)
        parsedArgs = await parsePortfolioArgs(context,args)
        print(parsedArgs)

        if(parsedArgs.command == 'add'):
            if(not(await isValidTicker(parsedArgs.ticker))):
                await context.send(content="Invalid Ticker Provided")
                return
                
            #add to the user's portfolio and returns the return message
            returnMessage = portfolio_add(parsedArgs)
            await context.send(content=returnMessage)
        elif(parsedArgs.command == 'show' or parsedArgs.command == 'p/l' or parsedArgs.command == 'pl'):
                await context.send(embed = portfolio_show(parsedArgs))
        elif(parsedArgs.command == 'remove'):
            if(not positionBelongsToUser(parsedArgs.positionID,context.author.id)):
                await context.send(content="That position does not belong to you")
                return
            removePosition(parsedArgs.positionID)
            await context.send(content="Position Removed")

   #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return
    
bot.run(DISCORD_TOKEN)
