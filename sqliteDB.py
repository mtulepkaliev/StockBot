#SQLite interaction functions for ticker information functions
#using a database allows for us to store data and not have to query yfinance as much

import sqlite3
from typing import *
import yfinance as yf

from settings import REFRESH_TIMEOUT_SEC
from decimal import Decimal

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
    print('Info received on ' + tickerText)
    tickerStats = ticker.info
    try:
        #retreive needed varaibles
        currentPrice = Decimal(tickerStats['currentPrice'])
    except KeyError as e:
        print(f'{e} not found in {tickerText}, is probably a fund')
        currentPrice = Decimal(ticker.history(period="1d", interval="1m").tail(1)['Close'].iloc[0])
    openPrice = Decimal(tickerStats['open'])
    priceChange = currentPrice - openPrice
    pctChange = priceChange / openPrice
    dayLow = Decimal(tickerStats['regularMarketDayLow'])
    dayHigh = Decimal(tickerStats['regularMarketDayHigh'])
    f2wkLow = Decimal(tickerStats['fiftyTwoWeekLow'])
    f2wkHigh = Decimal(tickerStats['fiftyTwoWeekHigh'])
    priceHint = int(tickerStats['priceHint'])
    try:
        shortName = tickerStats['shortName']
    except KeyError:
        print(f'{tickerText} has no shortName,trying longName')
        try:
            shortName = tickerStats['longName']
        except KeyError:
            shortName = tickerText
            print(f'{tickerText} has no longName,using symbol')

    try:
        website = tickerStats['website']
    except KeyError:
        website = None


    #insert into database
    cursor.execute(("REPLACE INTO Tickers "+
                    "(symbol,currentPrice,priceChange,percentChange,openPrice,lastRefresh,fiftyTwoWeekHigh,fiftyTwoWeekLow,dayHigh,dayLow,companyName,website,priceHint) " +
                    "VALUES(?,?,?,?,?,strftime('%s'),?,?,?,?,?,?,?)"),
                    (tickerText,str(currentPrice),str(priceChange),str(pctChange),str(openPrice),str(f2wkHigh),str(f2wkLow),str(dayHigh),str(dayLow),shortName,website,priceHint))
    con.commit()

    return
