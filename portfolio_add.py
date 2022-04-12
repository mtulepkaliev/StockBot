#File to add stocks to user's portfolio
from decimal import Decimal
from portfolio import *


def portfolio_add(user_id:str,ticker:str,price:Decimal,share_amt:int) -> str:

    #import portfolios json into local dictionary
    try:
        portfolio_dict = getPortfolioDict()
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
            new_avg_price = str((Decimal((amt_held * avgprice) + price*share_amt)/ new_share_amt))

            #write the new values into the dictionary
            portfolio_dict[user_id][ticker]['amount'] = new_share_amt
            portfolio_dict[user_id][ticker]['avgPrice'] = new_avg_price
            status_code = 1
    #write data back to json
    writePortfolio(portfolio_dict)
    return generateAddReturnMsg(status_code)

#turns status code into output for user, just returns status code for now
#TODO return more meaningful output to user
def generateAddReturnMsg(status_code) -> str:
    return status_code
