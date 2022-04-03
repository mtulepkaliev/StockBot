#File for functions invlolving most of the interaction with the Yahoo Finance API

import nextcord
import requests
import yfinance as yf
from nextcord.ext import *
from decimal import *

from portfolio_add import DECIMAL_FORMAT


def getPriceOutput(ticker_info:dict,args:tuple) -> nextcord.Embed:
    #save the part of the dict we need (for readability purposes)
    price_stats = ticker_info['price']

    #retreve needed varaibles
    price = Decimal(price_stats['regularMarketPrice']).quantize(DECIMAL_FORMAT)
    pricechange = Decimal(price_stats['regularMarketChange']).quantize(DECIMAL_FORMAT)
    pctchange = Decimal(price_stats['regularMarketChangePercent'] * 100).quantize(DECIMAL_FORMAT)

    pctchange = str(pctchange) + '%'

    #set embed color and prefix to proper ones for red and green days
    if (Decimal(pricechange) >= 0):   
        pricechange = '+' + str(pricechange)
        pctchange = '+' + pctchange
        embedColor = nextcord.Color.from_rgb(0,255,0)
    else:
        embedColor = nextcord.Color.from_rgb(255,0,0)


    #retreive needed output variables
    ticker_name = price_stats['symbol']
    short_name = price_stats['shortName']
    yfinurl = 'https://finance.yahoo.com/quote/' + str(ticker_name)
    footer_text = "Price data is delayed by 15 minutes"

    embed=nextcord.Embed(title=short_name, url=yfinurl, description=ticker_name, color=embedColor)
    embed.add_field(name="Price", value=price, inline=False)
    embed.add_field(name="Day Change", value=pricechange, inline=False)
    embed.add_field(name="Percent Change", value=pctchange, inline=False)

    #add ranges to embed if the user requested them
    if('-range' in args):
        #obtain variables
        daylow = Decimal(price_stats['regularMarketDayLow']).quantize(DECIMAL_FORMAT)
        dayhigh = Decimal(price_stats['regularMarketDayHigh']).quantize(DECIMAL_FORMAT)
        f2wklow = ticker_info['summaryDetail']['fiftyTwoWeekLow']
        f2wkhigh = ticker_info['summaryDetail']['fiftyTwoWeekHigh']

        #format strings
        day_range = f"{daylow} - {dayhigh}"
        fifty_two_week_range = f"{f2wklow} - {f2wkhigh}"

        #add to embed
        embed.add_field(name="Day Range", value=day_range, inline=False)
        embed.add_field(name="52 Week Range", value=fifty_two_week_range, inline=False)

    #code to include logo if possible and add attribution
    try:
        logo_url = 'https://logo.clearbit.com/' + str(ticker_info['summaryProfile']['website'])

        #add thumbnail and attribution if clearbit has a logo for the company (status 404 means no logo)
        if(requests.head(logo_url).status_code != 404):
            embed.set_thumbnail(url=logo_url)
            footer_text = footer_text + ', Logo provided by Clearbit.com'
        else:
            print("No logo avaliable for ticker " + ticker_name)

    #exception handling for if no webiste is provided by yfinance (Happens for ETF's and such)
    except KeyError:
        print("No website provided for ticker " + ticker_name)

    embed.set_footer(text=footer_text)

    return embed

async def isValidTicker(ticker_text:str,context):
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
