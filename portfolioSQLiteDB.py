#file for SQLite functions for portfolios

from decimal import Decimal
import sqlite3
import traceback

#establish connection and cursor to return rows
con = sqlite3.connect("portfolio.db")
con.execute("PRAGMA foreign_keys = ON;")
con.row_factory = sqlite3.Row
cursor = con.cursor()


def insertPosition(userID:int, ticker:str,avgPrice:Decimal,shareAmt:int) -> int:
    '''inserts a position into the positions table and returns status code based on success'''

    try:
        avgPrice:float = float(avgPrice)
        cursor.execute("INSERT INTO Positions (userID,symbol,purchasePrice,numShares) VALUES(?,?,?,?)",(userID,ticker,avgPrice,shareAmt))
        con.commit()
        return 1
    except Exception as e:
        traceback.print_exc()
        print(e)
        return 0

def getUserPositions(userID:int) -> list[int]:
    '''gets a list of position ID's that are held by a user'''
    
    #get the position ID's
    userPositions = cursor.execute("SELECT positionID FROM USER_POSITIONS WHERE userID = ?",(userID,)).fetchall()
    posList:list = []


    #convert to a list
    for position in userPositions:
        posList.append(position['positionID'])
    return posList


def getPositionInfo(positionID:int) -> sqlite3.Row:
    '''returns all the information on a single position'''

    position:sqlite3.Row = cursor.execute("SELECT * FROM USER_POSITIONS WHERE positionID = ?",(positionID,)).fetchone()
    return position
    
def getPositionInfoByStock(userID:int) -> list[sqlite3.Row]:
    '''returns all the positions held by a user grouped by the ticker'''

    position = cursor.execute('''
    SELECT
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
    GROUP BY symbol''',
    (userID,)).fetchall()
    return position
