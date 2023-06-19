#main bot function

import os
import traceback
from decimal import Decimal
from argparse import ArgumentParser

import nextcord
import yfinance as yf
from dotenv import load_dotenv
from nextcord.ext import commands
from portfolio import portfolio_add, portfolio_show
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
        #retreive user id and command
        userID:str = str(context.author.id) 
        command:str = args[0]

        parser = ArgumentParser()
        parser.add_argument('command',type=str)

        #add command
        if(command == 'add'):
            parser.add_argument('ticker',type=str)
            parser.add_argument('avgPrice',type=Decimal)
            parser.add_argument('shareAmt',type=int)

            parsedArgs = parser.parse_args(args)

            print(f"args:{parsedArgs}")
            #check for valid ticker
            if(not(await isValidTicker(parsedArgs.ticker))):
                await context.send(content="Invalid Ticker Provided")
                return
                
            #add to the user's portfolio and returns the return message
            returnMessage = portfolio_add(userID, parsedArgs)
            await context.send(content=returnMessage)
        if(command == 'show' or command == 'p/l' or command == 'pl'):

            #determine if the user requested another user's portfolio
            try:
                user:str = str(context.message.mentions[0].id)
                userName:str = context.message.mentions[0].display_name
            except IndexError as e:
                print(e)
                print("No user specified, defaulting to sender")
                user:str = str(context.author.id)
                userName:str = (context.author.display_name)

            # add mutually exclusive group of arguments
            showArgGroup = parser.add_mutually_exclusive_group()
            showArgGroup.add_argument('-n', '--net', action='store_true')
            showArgGroup.add_argument('-b', '--brief', action='store_true')
            showArgGroup.add_argument('-f', '--full', action='store_true')

            if(command == 'p/l' or command == 'pl'):
                timeArgGroup = parser.add_mutually_exclusive_group()
                timeArgGroup.add_argument('-d', '--day', action='store_true')
                timeArgGroup.add_argument('-t', '--total', action='store_true')
                #set the default to brief if no other option is selected, weird workaround
            #filter and convert args
            #argsList = checkShowArgs(context)

            try:
                parsedArgs = parser.parse_args(args)
            except SystemExit as exit:
                await context.send(content='Invalid Arguments Provided')
                return

            #set the default to brief if no other option is selected, weird workaround
            if not any([parsedArgs.net, parsedArgs.brief, parsedArgs.full]):
                parsedArgs.brief = True

            print(f"args:{parsedArgs}")
            if(command == 'show'):
                await context.send(embed = portfolio_show(user,userName,parsedArgs))
            elif(command == 'p/l' or command == 'pl'):
                if not any([parsedArgs.total]):
                    parsedArgs.day = True
                print(f"args:{parsedArgs}")
                await context.send(embed = portfolio_show(user,userName,parsedArgs))

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
