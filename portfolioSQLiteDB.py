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

def getUserPositions(user_id:int) -> list:
    userPositions = cursor.execute("SELECT positionID FROM USER_POSITIONS WHERE userID = ?",(user_id,)).fetchall()
    posList:list = []
    for position in userPositions:
        posList.append(position['positionID'])
    return posList
def getPositionInfo(position_id:int) -> sqlite3.Row:
    position = cursor.execute("SELECT * FROM USER_POSITIONS WHERE positionID = ?",(position_id,)).fetchone()
    return position
    
def getPositionInfoByStock(user_id:int) -> sqlite3.Row:
    position = cursor.execute('''SELECT
    symbol, 
    currentPrice, 
    openPrice,
    priceChange,
    total(purchasePrice * numShares)/total(numShares) AS "averagePrice",
    SUM(numShares) AS "totalShares",
    (total(purchasePrice * numShares)/total(numShares)) * SUM(numShares) AS "costBasis",
    dayPLPct,
    priceChange * SUM(numShares) AS "dayPL" 
    FROM USER_POSITIONS 
    WHERE userID=?
    GROUP BY symbol''',(user_id,)).fetchall()
    return position
