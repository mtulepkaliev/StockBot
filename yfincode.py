#File for functions invlolving most of the interaction with the Yahoo Finance API

from decimal import *
from sqlite3 import Row
from typing import Tuple
from argparse import Namespace
import nextcord
import requests
import yfinance as yf
from nextcord.ext import *
from settings import DOLLAR_FORMAT
from sqliteDB import getTickerInfo, hasTicker, updateTickerInfo

def decimalToPrecisionString(decimal:Decimal,precision:int) -> str:
    '''returns a string of a decimal with the given precision'''
    quanitzeFormat = Decimal(Decimal(10)**(-1 * precision))
    return f"{decimal.quantize(quanitzeFormat):.{precision}f}"

def getPriceOutput(args:Namespace) -> nextcord.Embed:
    '''returns the embed to output on a ticker's info'''
    
    tickerText:str = args.ticker
    #save the part of the dict we need (for readability purposes)
    tickerInfo:Row = getTickerInfo(tickerText)

    priceHint = int(tickerInfo['priceHint'])

    #retreve needed varaibles
    price = decimalToPrecisionString(Decimal(tickerInfo['currentPrice']),priceHint)
    priceChange:str = decimalToPrecisionString(Decimal(tickerInfo['priceChange']),priceHint)
    pctChange = Decimal(tickerInfo['percentChange'] * 100).quantize(DOLLAR_FORMAT)

    #print(Decimal(tickerInfo['priceChange']))
    #print(priceChange)

    pctChange = str(pctChange) + '%'

    #set embed color and prefix to proper ones for red and green days
    if (Decimal(priceChange) >= 0):
        priceChange = '+' + str(priceChange)
        pctChange = '+' + pctChange
        embedColor = nextcord.Color.from_rgb(0,255,0)
    else:
        embedColor = nextcord.Color.from_rgb(255,0,0)


    #retreive needed output variables
    tickerName = tickerInfo['symbol']
    shortName = tickerInfo['companyName']
    yfinURL = 'https://finance.yahoo.com/quote/' + str(tickerName)
    footerText = "Price data is delayed by 15 minutes"

    embed=nextcord.Embed(title=shortName, url=yfinURL, description=tickerName, color=embedColor)
    embed.add_field(name="Price", value=price, inline=False)

    
    embed.add_field(name="Day Change", value=priceChange, inline=False)
    embed.add_field(name="Percent Change", value=pctChange, inline=False)

    #add ranges to embed if the user requested them
    if(args.range):
        #obtain variables
        daylow = decimalToPrecisionString(Decimal(tickerInfo['dayLow']),priceHint)
        dayhigh = decimalToPrecisionString(Decimal(tickerInfo['dayHigh']),priceHint)
        f2wklow = decimalToPrecisionString(Decimal(tickerInfo['fiftyTwoWeekLow']),priceHint)
        f2wkhigh = decimalToPrecisionString(Decimal(tickerInfo['fiftyTwoWeekHigh']),priceHint)

        #format strings
        dayRange = f"{daylow} - {dayhigh}"
        fiftyTwoWeekRange = f"{f2wklow} - {f2wkhigh}"

        #add to embed
        embed.add_field(name="Day Range", value=dayRange, inline=False)
        embed.add_field(name="52 Week Range", value=fiftyTwoWeekRange, inline=False)

    #code to include logo if possible and add attribution
    if(tickerInfo['website'] != None):
        logoURL = 'https://logo.clearbit.com/' + str(tickerInfo['website'])

        #add thumbnail and attribution if clearbit has a logo for the company (status 404 means no logo)
        if(requests.head(logoURL).status_code != 404):
            embed.set_thumbnail(url=logoURL)
            footerText = footerText + ', Logo provided by Clearbit.com'
        else:
            print("No logo avaliable for ticker " + tickerName)
    else:
        print("No website provided for ticker " + tickerName)

    embed.set_footer(text=footerText)

    return embed

async def isValidTicker(tickerText:str):
    '''return true if the ticker is in the database, we make sure to only insert valid tickers, this prevents us from having to query yfinance'''

    if(hasTicker(tickerText)):
        return True

    try:
        ticker:yf.Ticker = yf.Ticker(tickerText)
        tickerStats:dict = ticker.info
        tickerStats['symbol']
        updateTickerInfo(tickerText)
    except requests.exceptions.HTTPError as e:
        #tell user they entered the wrong ticker
        print("Exception:" + str(e))
        return False
    else:
        return True
