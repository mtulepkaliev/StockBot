

import sqlite3
from decimal import Decimal
from portfolioSQLiteDB import insertPosition
from sqliteDB import hasTicker, updateTickerInfo

from userSQLiteDB import userCheck


def portfolio_add(user_id:int, ticker:str,avg_price:Decimal,share_amt:int) -> str:
    '''adds position to user's portfolio and returns message on if it was successful'''
    userCheck(user_id)
    if(not hasTicker(ticker)):
        updateTickerInfo(ticker)
    result:int = insertPosition(user_id,ticker,avg_price,share_amt)

    if(result == 1):
        return "Successfully added position"
    else:
        return "Unable to add to portfolio"