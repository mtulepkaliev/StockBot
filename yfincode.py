#File for functions invlolving most of the interaction with the Yahoo Finance API

from decimal import *
from sqlite3 import Row
from typing import Tuple
import nextcord
import requests
import yfinance as yf
from nextcord.ext import *
from settings import DECIMAL_FORMAT
from sqliteDB import getTickerInfo, hasTicker, updateTickerInfo


def getPriceOutput(tickerText:str,args:Tuple) -> nextcord.Embed:
    '''returns the embed to output on a ticker's info'''
    
    #save the part of the dict we need (for readability purposes)
    tickerInfo:Row = getTickerInfo(tickerText)

    #retreve needed varaibles
    price = Decimal(tickerInfo['currentPrice']).quantize(DECIMAL_FORMAT)
    priceChange = Decimal(tickerInfo['priceChange']).quantize(DECIMAL_FORMAT)
    pctChange = Decimal(tickerInfo['percentChange'] * 100).quantize(DECIMAL_FORMAT)

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
    if('-range' in args):
        #obtain variables
        daylow = Decimal(tickerInfo['dayLow']).quantize(DECIMAL_FORMAT)
        dayhigh = Decimal(tickerInfo['dayHigh']).quantize(DECIMAL_FORMAT)
        f2wklow = Decimal(tickerInfo['fiftyTwoWeekLow']).quantize(DECIMAL_FORMAT)
        f2wkhigh = Decimal(tickerInfo['fiftyTwoWeekHigh']).quantize(DECIMAL_FORMAT)

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

async def isValidTicker(tickerText:str,context):
    '''return true if the ticker is in the database, we make sure to only insert valid tickers, this prevents us from having to query yfinance'''

    if(hasTicker(tickerText)):
        return True

    try:
        ticker:yf.Ticker = yf.Ticker(tickerText)
        tickerStats:dict = ticker.info
        tickerStats['symbol']
        updateTickerInfo(tickerText)
    except KeyError as e:
        #tell user they entered the wrong ticker
        print("Exception:" + str(e))
        await context.send(content='Invalid Ticker, please try again')
        return False
    else:
        return True
