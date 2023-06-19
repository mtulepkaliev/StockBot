#file for portfolio functions

from decimal import Decimal
from argparse import Namespace
import nextcord

from portfolioSQLiteDB import (getPositionInfo, getPositionInfoByStock,
                               getUserPositions, insertPosition)
from settings import DOLLAR_FORMAT
from sqliteDB import hasTicker, updateTickerInfo, getTickerInfo
from userSQLiteDB import userCheck, userExists
from yfincode import decimalToPrecisionString


def portfolio_add(userID:int, parsedArgs:Namespace) -> str:
    '''adds position to user's portfolio and returns message on if it was successful'''

    ticker = parsedArgs.ticker
    userCheck(userID)
    if(not hasTicker(ticker)):
        updateTickerInfo(ticker)
    result:int = insertPosition(userID,ticker,parsedArgs.avgPrice,parsedArgs.shareAmt)

    if(result == 1):
        return "Successfully added position"
    else:
        return "Unable to add to portfolio"

def portfolio_show(userID:int,userName:str,showArgs:Namespace) -> nextcord.Embed:
    '''returns the user's portfolio as an embed'''

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