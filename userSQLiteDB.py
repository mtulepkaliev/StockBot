#File to interact with SQLite for users

import sqlite3



#establish connection and cursor to return rows
con = sqlite3.connect("portfolio.db")
con.execute("PRAGMA foreign_keys = ON;")
con.row_factory = sqlite3.Row
cursor = con.cursor()


def userCheck(userID:int) -> None:
    '''Checks if a user is in the database and adds them if they are not'''

    if(not userExists(userID)):
        cursor.execute("INSERT INTO Users (userID) VALUES (?)", (userID,))
        con.commit()
        return
    else:
        return

def userExists(userID:int) -> bool:
    '''Checks if a user is in the database'''

    user = cursor.execute("SELECT userID FROM Users WHERE userID = ?",(userID,)).fetchall()
    return user
