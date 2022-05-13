#file for portfolio functions

from decimal import Decimal

import nextcord

from portfolioSQLiteDB import (getPositionInfo, getPositionInfoByStock,
                               getUserPositions, insertPosition)
from settings import DECIMAL_FORMAT
from sqliteDB import hasTicker, updateTickerInfo
from userSQLiteDB import userCheck, userExists


def portfolio_add(userID:int, ticker:str,avgPrice:Decimal,shareAmt:int) -> str:
    '''adds position to user's portfolio and returns message on if it was successful'''

    userCheck(userID)
    if(not hasTicker(ticker)):
        updateTickerInfo(ticker)
    result:int = insertPosition(userID,ticker,avgPrice,shareAmt)

    if(result == 1):
        return "Successfully added position"
    else:
        return "Unable to add to portfolio"

def portfolio_show(userID:int,userName:str,args:list) -> nextcord.Embed:
    '''returns the user's portfolio as an embed'''

    #make sure the user exists
    if(not userExists(userID)):
        return nextcord.Embed(title="User does not have portfolio")
    
    print('portfolio requested for user ' + userID)
    embed=nextcord.Embed(title=f'{userName}\'s Portfolio')
    totalCostBasis:Decimal = 0

    if('-full' in args):

        #get list of position ID's held by the user
        userPostions = getUserPositions(userID)


        for position in userPostions:

            #get the info on that position
            positionInfo = getPositionInfo(position)

            #save needed variables
            positionId = positionInfo['positionID']
            ticker = positionInfo['symbol']
            numShares:int = int(positionInfo['numShares'])
            sharePrice:Decimal = Decimal(positionInfo['purchasePrice'])
            costBasis = Decimal(positionInfo['costBasis'])

            totalCostBasis += costBasis

            #add the position to the embed
            embed.add_field(name=f'Position #{positionId}', value= f'{ticker}:{numShares} shares for ${sharePrice} per share, total cost basis of ${costBasis}', inline=False)
        
        totalCostBasis.quantize(DECIMAL_FORMAT)

        #add the total cost basis to the beginning
        embed.insert_field_at(0,name="Total Cost basis",value=f'${totalCostBasis}')
        return embed

    if('-brief' in args or '-net' in args):

        #get a list of Rows for the user by stock
        userTickers = getPositionInfoByStock(userID)

        for ticker in userTickers:

            #save needed variables
            tickerName = ticker['symbol']
            numShares:int = int(ticker['totalShares'])
            avgPrice:Decimal = Decimal(ticker['averagePrice']).quantize(DECIMAL_FORMAT)
            costBasis = Decimal(ticker['costBasis']).quantize(DECIMAL_FORMAT)

            totalCostBasis += costBasis

            #add the ticker if we are showing all of the tickers
            if('-brief' in args):
                embed.add_field(name=tickerName, value= f'{numShares} shares @ an average of ${avgPrice} per share, total cost basis of {costBasis}', inline=False)
        totalCostBasis.quantize(DECIMAL_FORMAT)

        #add the total cost basis of to the beginning
        embed.insert_field_at(0,name="Total Cost basis",value=f'${totalCostBasis}')
        return embed


def checkShowArgs(context) -> list:
    '''checks if the args provided for portfolio_show are valid and returns them'''

    #list of valid arguments
    rangeArgs:list = ["-day","-open"]
    displayArgs:list = ["-net","-brief","-full"]

    #remove show from the list of args
    args = context.args[1:]

    #convert all provided args to lowercase
    args = [s.lower() for s in args]

    #check if all provided args are valid
    for arg in args[:]:
        #remove the user arg if it was provided
        if(arg.startswith("<@")):
            args.remove(arg)
            continue
        if(((not arg in rangeArgs) and (not arg in displayArgs)) or (args.count(arg) != 1)):
            print(arg)
            raise ValueError("Invalid argument provided or multiple of one argument provided")
        if(len(set(args).intersection(set(rangeArgs))) > 1):
            print(arg)
            raise ValueError("Too many range arguments provided")
        if(len(set(args).intersection(set(displayArgs))) > 1):
            print(arg)
            raise ValueError("Too many display arguments provided")
     
    #add default arguments if no range or display arguments were given
    if(len(set(args).intersection(set(rangeArgs))) == 0):
        args.append("-day")
    if(len(set(args).intersection(set(displayArgs))) == 0):
        args.append("-brief")

    return args
