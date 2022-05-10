import sqlite3



#establish connection and cursor to return rows
con = sqlite3.connect("portfolio.db")
con.execute("PRAGMA foreign_keys = ON;")
con.row_factory = sqlite3.Row
cursor = con.cursor()


def userCheck(user_id:int) -> None:
    '''Checks if a user is in the database and adds them if they are not'''
    user = cursor.execute("SELECT userID FROM Users WHERE userID = ?",(user_id,)).fetchall()

    if(not user):
        cursor.execute("INSERT INTO Users (userID) VALUES (?)", (user_id,))
        con.commit()
        return
    else:
        return