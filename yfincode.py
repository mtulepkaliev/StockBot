#Seperate file for getting information from Yahoo finance, not using yet as ticker.info returns large dict and i don't wanna call it ech time as could be slow

import yfinance as yf
import json
from decimal import *

def getPriceOutput(ticker_info):
    decFormat = Decimal('0.01')
    price = Decimal(ticker_info['regularMarketPrice'])
    open = Decimal(ticker_info['open'])
    pricechange = (price - open).quantize(decFormat)
    pctchange = ((pricechange / open) * 100).quantize(decFormat)
    pctchange = str(pctchange) + '%'
    if (Decimal(pricechange) >= 0):   
        pricechange = '+' + str(pricechange)
        pctchange = '+' + pctchange
    output = f"{ticker_info['shortName']} ({ticker_info['symbol']}) {price.quantize(decFormat)} {pricechange} {pctchange}"
    return output