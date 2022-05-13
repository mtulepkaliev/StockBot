#File for functions invlolving most of the interaction with the Yahoo Finance API

from decimal import *
from sqlite3 import Row
from typing import Tuple
import nextcord
import requests
import yfinance as yf
from nextcord.ext import *
from settings import DECIMAL_FORMAT
from sqliteDB import getTickerInfo, hasTicker


def getPriceOutput(tickerText:str,args:Tuple) -> nextcord.Embed:
    '''returns the embed to output on a ticker's info'''
    
    #save the part of the dict we need (for readability purposes)
    tickerInfo:Row = getTickerInfo(tickerText)

    #retreve needed varaibles
    price = Decimal(tickerInfo['currentPrice']).quantize(DECIMAL_FORMAT)
    pricechange = Decimal(tickerInfo['priceChange']).quantize(DECIMAL_FORMAT)
    pctchange = Decimal(tickerInfo['percentChange'] * 100).quantize(DECIMAL_FORMAT)

    pctchange = str(pctchange) + '%'

    #set embed color and prefix to proper ones for red and green days
    if (Decimal(pricechange) >= 0):   
        pricechange = '+' + str(pricechange)
        pctchange = '+' + pctchange
        embedColor = nextcord.Color.from_rgb(0,255,0)
    else:
        embedColor = nextcord.Color.from_rgb(255,0,0)


    #retreive needed output variables
    ticker_name = tickerInfo['symbol']
    short_name = tickerInfo['companyName']
    yfinurl = 'https://finance.yahoo.com/quote/' + str(ticker_name)
    footer_text = "Price data is delayed by 15 minutes"

    embed=nextcord.Embed(title=short_name, url=yfinurl, description=ticker_name, color=embedColor)
    embed.add_field(name="Price", value=price, inline=False)
    embed.add_field(name="Day Change", value=pricechange, inline=False)
    embed.add_field(name="Percent Change", value=pctchange, inline=False)

    #add ranges to embed if the user requested them
    if('-range' in args):
        #obtain variables
        daylow = Decimal(tickerInfo['dayLow']).quantize(DECIMAL_FORMAT)
        dayhigh = Decimal(tickerInfo['dayHigh']).quantize(DECIMAL_FORMAT)
        f2wklow = Decimal(tickerInfo['fiftyTwoWeekLow']).quantize(DECIMAL_FORMAT)
        f2wkhigh = Decimal(tickerInfo['fiftyTwoWeekHigh']).quantize(DECIMAL_FORMAT)

        #format strings
        day_range = f"{daylow} - {dayhigh}"
        fifty_two_week_range = f"{f2wklow} - {f2wkhigh}"

        #add to embed
        embed.add_field(name="Day Range", value=day_range, inline=False)
        embed.add_field(name="52 Week Range", value=fifty_two_week_range, inline=False)

    #code to include logo if possible and add attribution
    if(tickerInfo['website'] != None):
        logo_url = 'https://logo.clearbit.com/' + str(tickerInfo['website'])

        #add thumbnail and attribution if clearbit has a logo for the company (status 404 means no logo)
        if(requests.head(logo_url).status_code != 404):
            embed.set_thumbnail(url=logo_url)
            footer_text = footer_text + ', Logo provided by Clearbit.com'
        else:
            print("No logo avaliable for ticker " + ticker_name)
    else:
        print("No website provided for ticker " + ticker_name)

    embed.set_footer(text=footer_text)

    return embed

async def isValidTicker(ticker_text:str,context):
    '''return true if the ticker is in the database, we make sure to only insert valid tickers, this prevents us from having to query yfinance'''

    if(hasTicker(ticker_text)):
        return True

    try:
        ticker:yf.Ticker = yf.Ticker(ticker_text)
        ticker_stats:dict = ticker.stats()
        ticker_stats['price']['regularMarketPrice']
    except KeyError as e:
        #tell user they entered the wrong ticker
        print("Exception:" + str(e))
        await context.send(content='Invalid Ticker, please try again')
        return False
    else:
        return True
