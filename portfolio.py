#file for portfolio functions

from decimal import Decimal
from argparse import Namespace, ArgumentParser
import nextcord

from portfolioSQLiteDB import (getPositionInfo, getPositionInfoByStock,
                               getUserPositions, insertPosition)
from settings import DOLLAR_FORMAT
from sqliteDB import hasTicker, updateTickerInfo, getTickerInfo
from userSQLiteDB import userCheck, userExists
from yfincode import decimalToPrecisionString


def portfolio_add(parsedArgs:Namespace) -> str:
    '''adds position to user's portfolio and returns message on if it was successful'''
    userID:str = parsedArgs.userID
    ticker = parsedArgs.ticker
    userCheck(userID)
    if(not hasTicker(ticker)):
        updateTickerInfo(ticker)
    result:int = insertPosition(userID,ticker,parsedArgs.avgPrice,parsedArgs.shareAmt)

    if(result == 1):
        return "Successfully added position"
    else:
        return "Unable to add to portfolio"

def portfolio_show(showArgs:Namespace) -> nextcord.Embed:
    '''returns the user's portfolio as an embed'''
    userID = showArgs.userID
    userName = showArgs.userName

    profitLoss:bool = (showArgs.command == 'pl' or showArgs.command == 'p/l')
        
    #make sure the user exists
    if(not userExists(userID)):
        return nextcord.Embed(title="User does not have portfolio")
    
    if(getUserPositions(userID) == None):
        return nextcord.Embed(title="User's portfolio is empty")
    print('portfolio requested for user ' + userID)
    embed=nextcord.Embed(title=f'{userName}\'s Portfolio')
    totalCostBasis:Decimal = Decimal(0)
    totalPortfolioMarketValue:Decimal = Decimal(0)

    if(showArgs.full):

        #get list of position ID's held by the user
        userPostions = getUserPositions(userID)

        for position in userPostions:

            #get the info on that position
            positionInfo = getPositionInfo(position)

            #save needed variables
            positionId = positionInfo['positionID']
            ticker = positionInfo['symbol']
            numShares:int = int(positionInfo['numShares'])

            priceHint:int = positionInfo['priceHint']
            sharePriceFormat = Decimal(Decimal(10)**(-1 * priceHint))

            sharePrice:Decimal = Decimal(positionInfo['purchasePrice'])
            costBasis:Decimal = Decimal(positionInfo['costBasis']).quantize(DOLLAR_FORMAT)

            totalCostBasis += costBasis

            if(not profitLoss):
                #add the position to the embed
                embed.add_field(name=f'Position #{positionId}', value= f'{ticker}:{numShares} shares for ${decimalToPrecisionString(sharePrice,priceHint)} per share, total cost basis of ${costBasis}', inline=False)
            else:
                #get the current price of the stock
                currentPrice = Decimal(getTickerInfo(ticker)['currentPrice'])
                #calculate the profit/loss
                profitLoss = Decimal((currentPrice - sharePrice) * numShares).quantize(DOLLAR_FORMAT)
                #calculate the percent profit/loss
                percentProfitLoss = Decimal((profitLoss / costBasis) * 100).quantize(DOLLAR_FORMAT)
                #add the position to the embed
                embed.add_field(name=f'Position #{positionId}', value= f'{ticker}:{numShares} shares for ${decimalToPrecisionString(sharePrice,priceHint)} per share, total cost basis of ${costBasis}, current profit/loss of ${profitLoss} ({percentProfitLoss}%)', inline=False)

                totalPortfolioMarketValue += Decimal(currentPrice * numShares).quantize(DOLLAR_FORMAT)
        
        totalCostBasis.quantize(DOLLAR_FORMAT)

        #add the total cost basis to the beginning
        embed.insert_field_at(0,name="Total Cost basis",value=f'${totalCostBasis}')
        if(profitLoss):
            totalProfitLoss:Decimal = Decimal(totalPortfolioMarketValue - totalCostBasis).quantize(DOLLAR_FORMAT)
            totalPercentProfitLoss:Decimal = Decimal((totalProfitLoss / totalCostBasis) * 100).quantize(DOLLAR_FORMAT)
            embed.insert_field_at(1,name="Total Profit/Loss",value=f'${totalProfitLoss} ({totalPercentProfitLoss}%)')
        return embed

    if(showArgs.brief or showArgs.net):

        #get a list of Rows for the user by stock
        userTickers = getPositionInfoByStock(userID)

        for ticker in userTickers:

            #save needed variables
            tickerName = ticker['symbol']
            numShares:int = int(ticker['totalShares'])
            avgPrice:Decimal = Decimal(ticker['averagePrice'])
            costBasis = Decimal(ticker['costBasis']).quantize(DOLLAR_FORMAT)

            priceHint:int = ticker['priceHint']
            sharePriceFormat = Decimal(Decimal(10)**(-1 * priceHint))

            totalCostBasis += costBasis

            #add the ticker if we are showing all of the tickers
            if(profitLoss):
                currentPrice:Decimal = Decimal(getTickerInfo(tickerName)['currentPrice'])
                profitLoss:Decimal = Decimal((currentPrice - avgPrice) * numShares).quantize(DOLLAR_FORMAT)
                percentProfitLoss:Decimal = Decimal((profitLoss / costBasis) * 100).quantize(DOLLAR_FORMAT)

                totalPortfolioMarketValue += Decimal(currentPrice * numShares).quantize(DOLLAR_FORMAT)
                if(showArgs.brief):
                    embed.add_field(name=tickerName, value= f'{numShares} shares @ an average of ${decimalToPrecisionString(avgPrice,priceHint)} per share, total cost basis of {costBasis}, current profit/loss of ${profitLoss} ({percentProfitLoss}%)', inline=False)
            elif(showArgs.brief):
                embed.add_field(name=tickerName, value= f'{numShares} shares @ an average of ${decimalToPrecisionString(avgPrice,priceHint)} per share, total cost basis of {costBasis}', inline=False)
        totalCostBasis.quantize(DOLLAR_FORMAT)

        #add the total cost basis of to the beginning
        embed.insert_field_at(0,name="Total Cost basis",value=f'${totalCostBasis}')
        if(profitLoss):
            totalProfitLoss:Decimal = Decimal(totalPortfolioMarketValue - totalCostBasis).quantize(DOLLAR_FORMAT)
            totalPercentProfitLoss:Decimal = Decimal((totalProfitLoss / totalCostBasis) * 100).quantize(DOLLAR_FORMAT)
            embed.insert_field_at(1,name="Total Profit/Loss",value=f'${totalProfitLoss} ({totalPercentProfitLoss}%)')
        return embed
    
async def parsePortfolioArgs(context,args:tuple) -> Namespace:
    '''parses the arguments for the portfolio commands'''
    command:str = args[0]

    parser = ArgumentParser()
    parser.add_argument('command',type=str)

    #add command
    if(command == 'remove'):
        parser.add_argument('positionID',type=int)
        return parser.parse_args(args)
    if(command == 'add'):
        parser.add_argument('ticker',type=str)
        parser.add_argument('avgPrice',type=Decimal)
        parser.add_argument('shareAmt',type=int)

        parsedArgs = parser.parse_args(args)
        parsedArgs.userID = str(context.author.id)
        return parsedArgs
    if(command == 'show' or command == 'p/l' or command == 'pl'):
        
        # add positional argument for the user mention that may be included
        parser.add_argument('user',type=str,nargs='?',default=None)
        # add mutually exclusive group of arguments for what to show
        showArgGroup = parser.add_mutually_exclusive_group()
        showArgGroup.add_argument('-n', '--net', action='store_true')
        showArgGroup.add_argument('-b', '--brief', action='store_true')
        showArgGroup.add_argument('-f', '--full', action='store_true')

        if(command == 'p/l' or command == 'pl'):
            timeArgGroup = parser.add_mutually_exclusive_group()
            timeArgGroup.add_argument('-d', '--day', action='store_true')
            timeArgGroup.add_argument('-t', '--total', action='store_true')
        #filter and convert args
        #argsList = checkShowArgs(context)

        try:
            parsedArgs = parser.parse_args(args)
        except SystemExit as exit:
            raise Exception("Invalid Arguments Provided")

        #set the default to brief if no other option is selected, weird workaround
        if not any([parsedArgs.net, parsedArgs.brief, parsedArgs.full]):
            parsedArgs.brief = True

        if(command == 'p/l' or command == 'pl'):
            if not any([parsedArgs.total,parsedArgs.day]):
                parsedArgs.day = True

        #determine if the user requested another user's portfolio
        try:
            user:str = str(context.message.mentions[0].id)
            userName:str = context.message.mentions[0].display_name
        except IndexError as e:
            print(e)
            print("No user specified, defaulting to sender")
            user:str = str(context.author.id)
            userName:str = (context.author.display_name)
        parsedArgs.userID = user
        parsedArgs.userName = userName
        return parsedArgs