#File for functions involving handing of locally stored user portfolios
import json
from decimal import Decimal
from fileinput import close

import nextcord

#I know, global variable bad, but it's a constant,ok
global DECIMAL_FORMAT
DECIMAL_FORMAT = Decimal('0.01')

def portfolio_add(user_id:str,ticker:str,price:Decimal,share_amt:int) -> str:

    #import portfolios json into local dictionary
    try:
        with open('portfolio.json','r') as portfolio_json:
            portfolio_dict:dict = json.load(portfolio_json)
            portfolio_json.close()
    except FileNotFoundError:
        portfolio_dict = {}
    
    #test if the user is in the dictioanry
    try:
        portfolio_dict[user_id]
    #adds the user with information into the portfolio dictionary (returns code 100 for new user)
    except KeyError:
        
        print('user ID not found')
        info_to_add:dict = {
            user_id:{
                ticker:{
                    "amount": share_amt,
                    "avgPrice": str(price)
                }
            }
        }
        portfolio_dict.update(info_to_add)
        status_code = 100
    else:
        #test if the ticker is in the dicitoanry
        try:
            portfolio_dict[user_id][ticker]
        #add the ticker into the dictionary(returns code 1000 for new ticker)
        except KeyError:
            info_to_add:dict = {
                "amount": share_amt,
                "avgPrice": str(price)
            }
            portfolio_dict[user_id][ticker] = info_to_add
            status_code = 1000
        #if the program runs into an unexpected exception, exit out of the function as to avoid improperly writing to json
        except Exception as e:
            print(e)
            return "Unknown exception occured, please try again"
        #update the eixsting ticker value for that user (returns code 1)
        else:
            #code to update the listing if the ticker is already in the user's dictionary
            amt_held:int = portfolio_dict[user_id][ticker]['amount']
            avgprice:Decimal = Decimal(portfolio_dict[user_id][ticker]['avgPrice'])

            #calculate the new average share price and total amount of shares held
            new_share_amt = amt_held + share_amt
            new_avg_price = str((Decimal((amt_held * avgprice) + price*share_amt)/ new_share_amt).quantize(DECIMAL_FORMAT))

            #write the new values into the dictionary
            portfolio_dict[user_id][ticker]['amount'] = new_share_amt
            portfolio_dict[user_id][ticker]['avgPrice'] = new_avg_price
            status_code = 1
    #write data back to json
    with open('portfolio.json','w') as portfolio_json:
        json.dump(portfolio_dict,portfolio_json)
        portfolio_json.close()  
    return generateAddReturnMsg(status_code)

def portfolio_show(user_id:str,user_name:str) -> nextcord.Embed:
    with open('portfolio.json','r') as portfolio_json:
        portfolio_dict:dict = json.load(portfolio_json)
        portfolio_json.close()
    
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

#turns status code into output for user, just returns status code for now
#TODO return more meaningful output to user
def generateAddReturnMsg(status_code) -> str:
    return status_code
