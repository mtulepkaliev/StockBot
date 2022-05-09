from contextlib import closing
from decimal import Decimal
import sqlite3
from typing import *
import yfinance as yf

from settings import REFRESH_TIMEOUT_SEC


con = sqlite3.connect("portfolio.db")
con.row_factory = sqlite3.Row
cursor = con.cursor()

#returns a ticker's info as a Row given the string
def getTickerInfo(tickerText:str) -> sqlite3.Row:
    sqlQuery:str = "SELECT * FROM Tickers WHERE symbol = ?"
    info:list = cursor.execute(sqlQuery,(tickerText,)).fetchall()
    if(not hasTicker(tickerText)):
        print(tickerText + " not found in table, adding entry")
        updateTickerInfo(tickerText,())
    secondsSinceUpdate:int = int(cursor.execute("SELECT strftime('%s') - lastRefresh FROM Tickers WHERE symbol = ?",(tickerText,)).fetchone()[0])
    print("secSinceUpdate:" + str(secondsSinceUpdate))
    if(secondsSinceUpdate > REFRESH_TIMEOUT_SEC):
        print("Updating info on " + tickerText)
        updateTickerInfo(tickerText,())
    info:list = cursor.execute(sqlQuery,(tickerText,)).fetchone()
    return info

def hasTicker(tickerText:str) -> bool:
    sqlQuery:str = "SELECT * FROM Tickers WHERE symbol = ?"
    info:list = cursor.execute(sqlQuery,(tickerText,)).fetchall()
    if(not info):
        return False
    return True

def updateTickerInfo(tickerText:str,args:Tuple) -> None:
    ticker = yf.Ticker(tickerText)
    ticker_stats:dict = ticker.stats()
    print('Info received on ' + tickerText)
    #save the part of the dict we need (for readability purposes)
    price_stats = ticker_stats['price']

    #retreve needed varaibles
    currentPrice = float(price_stats['regularMarketPrice'])
    priceChange = float(price_stats['regularMarketChange'])
    pctChange = float(price_stats['regularMarketChangePercent'])
    openPrice = float(price_stats['regularMarketOpen'])
    daylow = float(price_stats['regularMarketDayLow'])
    dayhigh = float(price_stats['regularMarketDayHigh'])
    f2wklow = ticker_stats['summaryDetail']['fiftyTwoWeekLow']
    f2wkhigh = ticker_stats['summaryDetail']['fiftyTwoWeekHigh']
    short_name = price_stats['shortName']
    try:
        website = ticker_stats['summaryProfile']['website']
    except KeyError:
        website = None
    cursor.execute("REPLACE INTO Tickers(symbol,currentPrice,priceChange,percentChange,openPrice,lastRefresh,fiftyTwoWeekHigh,fiftyTwoWeekLow,dayHigh,dayLow,companyName,website) VALUES(?,?,?,?,?,strftime('%s'),?,?,?,?,?,?)",
                (tickerText,currentPrice,priceChange,pctChange,openPrice,f2wkhigh,f2wklow,dayhigh,daylow,short_name,website))
    con.commit()

    return
