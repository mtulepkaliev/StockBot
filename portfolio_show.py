import nextcord
import json
from decimal import Decimal
from portfolio import *


def portfolio_show(user_id:str,user_name:str) -> nextcord.Embed:
    portfolio_dict = getPortfolioDict()
    
    #test if user has a portfolio
    try:
        portfolio_dict[user_id]
    except KeyError:
        embed=nextcord.Embed(title='User Does Not Have a Portfolio')
        return embed
    print('portfolio requested for user ' + user_id)
    embed=nextcord.Embed(title=f'{user_name}\'s Portfolio')
    total_cost_basis:Decimal = 0
    num_stocks:int = 0

    for ticker in portfolio_dict[user_id]:
        num_shares:int = int(portfolio_dict[user_id][ticker]['amount'])
        avgPrice:Decimal = Decimal(portfolio_dict[user_id][ticker]['avgPrice'])
        cost_basis = Decimal(avgPrice * num_shares).quantize(DECIMAL_FORMAT)

        num_stocks += 1
        total_cost_basis += cost_basis
        embed.add_field(name=str(ticker), value= f'{num_shares} shares @ an average of ${avgPrice} per share, total cost basis of {cost_basis}', inline=False)
    embed.insert_field_at(0,name="Total Cost basis",value=f'${total_cost_basis}')
    return embed