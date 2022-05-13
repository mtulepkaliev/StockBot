from decimal import Decimal

import nextcord

from portfolioSQLiteDB import (getPositionInfo, getPositionInfoByStock,
                               getUserPositions, insertPosition)
from settings import DECIMAL_FORMAT
from sqliteDB import hasTicker, updateTickerInfo
from userSQLiteDB import userCheck, userExists


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

def portfolio_show(user_id:int,user_name:str,args:list) -> nextcord.Embed:
    if(not userExists(user_id)):
        return nextcord.Embed(title="User does not have portfolio")
    
    print('portfolio requested for user ' + user_id)
    embed=nextcord.Embed(title=f'{user_name}\'s Portfolio')
    total_cost_basis:Decimal = 0

    if('-full' in args):
        userPostions = getUserPositions(user_id)
        for position in userPostions:
            position_info = getPositionInfo(position)
            ticker = position_info['symbol']
            num_shares:int = int(position_info['numShares'])
            sharePrice:Decimal = Decimal(position_info['purchasePrice'])
            cost_basis = Decimal(sharePrice * num_shares)

            total_cost_basis += cost_basis
            total_cost_basis.quantize(DECIMAL_FORMAT)
            embed.add_field(name=ticker, value= f'{num_shares} shares for ${sharePrice} per share, total cost basis of ${cost_basis}', inline=False)
        embed.insert_field_at(0,name="Total Cost basis",value=f'${total_cost_basis}')
        return embed
    if('-brief' in args or '-net' in args):
        userTickers = getPositionInfoByStock(user_id)
        for ticker in userTickers:
            ticker_name = ticker['symbol']
            num_shares:int = int(ticker['totalShares'])
            avgPrice:Decimal = Decimal(ticker['averagePrice']).quantize(DECIMAL_FORMAT)
            cost_basis = Decimal(ticker['costBasis']).quantize(DECIMAL_FORMAT)

            total_cost_basis += cost_basis
            if('-brief' in args):
                embed.add_field(name=ticker_name, value= f'{num_shares} shares @ an average of ${avgPrice} per share, total cost basis of {cost_basis}', inline=False)
        total_cost_basis.quantize(DECIMAL_FORMAT)
        embed.insert_field_at(0,name="Total Cost basis",value=f'${total_cost_basis}')
        return embed


def checkShowArgs(context) -> list:
    '''checks if the args provided for portfolio_show are valid and returns them'''
    #list of valid arguments
    rangeArgs:list = ["-day","-open"]
    displayArgs:list = ["-net","-brief","-full"]

    args = context.args[1:]

    #remove show from list of args
    args.remove("show")

    #convert all provided args to lowercase
    args = [s.lower() for s in args]

    #check if all provided args are valid
    for arg in args[:]:
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
     

    if(len(set(args).intersection(set(rangeArgs))) == 0):
        args.append("-day")
    if(len(set(args).intersection(set(displayArgs))) == 0):
        args.append("-brief")
    return args
