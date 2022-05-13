#SQLite interaction functions for ticker information functions
#using a database allows for us to store data and not have to query yfinance as much

import sqlite3
from typing import *
import yfinance as yf

from settings import REFRESH_TIMEOUT_SEC

#establish connection and cursor to return rows
con = sqlite3.connect("portfolio.db")
con.execute("PRAGMA foreign_keys = ON;")
con.row_factory = sqlite3.Row
cursor = con.cursor()


def getTickerInfo(tickerText:str) -> sqlite3.Row:
    '''returns a ticker's info from database as a Row given the string'''

    sqlQuery:str = "SELECT * FROM Tickers WHERE symbol = ?"

    #if there is no data add the ticker data to the database
    if(not hasTicker(tickerText)):
        print(tickerText + " not found in table, adding entry")
        updateTickerInfo(tickerText)

    checkTickerRefresh(tickerText)
    info:list = cursor.execute(sqlQuery,(tickerText,)).fetchone()
    return info


def hasTicker(tickerText:str) -> bool:
    '''returns true/false on whether or not a ticker exists in the database'''
    sqlQuery:str = "SELECT * FROM Tickers WHERE symbol = ?"
    info:list = cursor.execute(sqlQuery,(tickerText,)).fetchall()
    
    #if the returned list was empty the ticker is not in the table
    if(not info):
        return False
    return True


def checkTickerRefresh(tickerText:str) -> None:
    '''checks if the ticker has been updated and udates it if it is too far out of date'''


    #calculate how long it has been since the ticker was last updated
    secondsSinceUpdate:int = int(cursor.execute("SELECT strftime('%s') - lastRefresh FROM Tickers WHERE symbol = ?",(tickerText,)).fetchone()[0])
    print("secSinceUpdate:" + str(secondsSinceUpdate))

    #update the ticker info if it is too far out of date
    if(secondsSinceUpdate > REFRESH_TIMEOUT_SEC):
        print("Updating info on " + tickerText)
        updateTickerInfo(tickerText)
    return


def updateTickerInfo(tickerText:str) -> None:
    '''updates the ticker info in the database'''
    ticker = yf.Ticker(tickerText)
    ticker_stats:dict = ticker.stats()
    print('Info received on ' + tickerText)

    #save the part of the dict we need (for readability purposes)
    price_stats = ticker_stats['price']

    #retreive needed varaibles
    currentPrice = float(price_stats['regularMarketPrice'])
    priceChange = float(price_stats['regularMarketChange'])
    pctChange = float(price_stats['regularMarketChangePercent'])
    openPrice = float(price_stats['regularMarketOpen'])
    daylow = float(price_stats['regularMarketDayLow'])
    dayhigh = float(price_stats['regularMarketDayHigh'])
    f2wklow = float(ticker_stats['summaryDetail']['fiftyTwoWeekLow'])
    f2wkhigh = float(ticker_stats['summaryDetail']['fiftyTwoWeekHigh'])
    short_name = price_stats['shortName']

    #adds the website if there is one
    try:
        website = ticker_stats['summaryProfile']['website']
    except KeyError:
        website = None


    #insert into database
    cursor.execute(("REPLACE INTO Tickers "+
                    "(symbol,currentPrice,priceChange,percentChange,openPrice,lastRefresh,fiftyTwoWeekHigh,fiftyTwoWeekLow,dayHigh,dayLow,companyName,website) " +
                    "VALUES(?,?,?,?,?,strftime('%s'),?,?,?,?,?,?)"),
                    (tickerText,currentPrice,priceChange,pctChange,openPrice,f2wkhigh,f2wklow,dayhigh,daylow,short_name,website))
    con.commit()

    return
