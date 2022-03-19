#Seperate file for getting information from Yahoo finance, not using yet as ticker.info returns large dict and i don't wanna call it ech time as could be slow

import yfinance as yf
import json
from decimal import *

def getPriceOutput(ticker_info):

    #save the part of the dict we need (for readability purposes)
    price_stats = ticker_info['price']

    decFormat = Decimal('0.01')

    #retreve needed varaibles
    price = Decimal(price_stats['regularMarketPrice']).quantize(decFormat)
    pricechange = Decimal(price_stats['regularMarketChange']).quantize(decFormat)
    pctchange = Decimal(price_stats['regularMarketChangePercent'] * 100).quantize(decFormat)

    pctchange = str(pctchange) + '%'

    if (Decimal(pricechange) >= 0):   
        pricechange = '+' + str(pricechange)
        pctchange = '+' + pctchange
    output = f"{price_stats['shortName']} ({price_stats['symbol']}) \nPrice: {price} \nDay Change: {pricechange}\nPercent Change: {pctchange}"
    return output