#Seperate file for getting information from Yahoo finance, not using yet as ticker.info returns large dict and i don't wanna call it ech time as could be slow


import yfinance as yf
import json
from decimal import *

def getPriceOutput(ticker_info):
    ticker = ticker_info['symbol']
    name = ticker_info['shortName']
    currentPrice = ticker_info['regularMarketPrice']
    openPrice = ticker_info['open']
    pricechange = Decimal((Decimal(currentPrice) - Decimal(openPrice)))
    pctchange = Decimal(((pricechange/Decimal(openPrice)) * 100))
    pricechange = str(pricechange.quantize(Decimal('0.01')))
    pctchange = str(pctchange.quantize(Decimal('0.01'))) + '%'
    if(Decimal(pricechange) >= 0):   
        pricechange = '+' + pricechange
        pctchange = '+' + pctchange
    output = (str(name) + ' (' + str(ticker) + '): ' + str(Decimal(currentPrice).quantize(Decimal('0.01'))) + '  ' + pricechange + '  ' + pctchange)
    return output