#main bot function

import os
import traceback
from decimal import Decimal

import nextcord
import yfinance as yf
from dotenv import load_dotenv
from nextcord.ext import commands
from portfolio import checkShowArgs, portfolio_add, portfolio_show
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
    print("asked for price")
    tickerName:str = args[0]
    print('Ticker Requested:' + tickerName)
    try:
        #returns data if the ticker is valid
        if(await isValidTicker(tickerName,context)):
            await context.send(embed=getPriceOutput(tickerName,args[1:len(args)]))

    #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return

@bot.command()
async def portfolio(context,*args):
    try:
        #retreive user id and command
        userID:str = str(context.author.id) 
        command:str = args[0]

        #add command
        if(command == 'add'):
            #retreive variables from args
            ticker:str = args[1]
            avgPrice:Decimal = Decimal(args[2])
            shareAmt:int = int(args[3])

            #check for valid ticker
            if(not(await isValidTicker(ticker,context))):
                await context.send(content="Invalid Ticker Provided")
                return
                
            #add to the user's portfolio and returns the return message
            returnMessage = portfolio_add(userID, ticker,avgPrice,shareAmt)
            await context.send(content=returnMessage)
        if(command == 'show'):

            #determine if the user requested another user's portfolio
            try:
                user:str = str(context.message.mentions[0].id)
                userName:str = context.message.mentions[0].display_name
            except IndexError as e:
                print(e)
                print("No user specified, defaulting to sender")
                user:str = str(context.author.id)
                userName:str = (context.author.display_name)

            #filter and convert args
            argsList = checkShowArgs(context)


            await context.send(embed = portfolio_show(user,userName,argsList))
        if(command == 'remove'):
            positionID:int = args[1]
            if(not positionBelongsToUser(positionID,context.author.id)):
                await context.send(content="That position does not belong to you")
                return
            removePosition(positionID)
            await context.send(content="Position Removed")

   #print unknown exeception for all other exceptions
    except Exception as e:
        traceback.print_exc()
        await context.send(content='Unknown Exception Occured, Please Try Again')
        return
    
bot.run(DISCORD_TOKEN)
