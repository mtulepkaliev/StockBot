from decimal import Decimal
import sqlite3
import traceback

#establish connection and cursor to return rows
con = sqlite3.connect("portfolio.db")
con.execute("PRAGMA foreign_keys = ON;")
con.row_factory = sqlite3.Row
cursor = con.cursor()


def insertPosition(user_id:int, ticker:str,avg_price:Decimal,share_amt:int) -> int:
    '''inserts a position into the positions table and returns status code based on success'''
    try:
        avg_price:float = float(avg_price)
        cursor.execute("INSERT INTO Positions (userID,symbol,purchasePrice,numShares) VALUES(?,?,?,?)",(user_id,ticker,avg_price,share_amt))
        con.commit()
        return 1
    except Exception as e:
        traceback.print_exc()
        print(e)
        return 0