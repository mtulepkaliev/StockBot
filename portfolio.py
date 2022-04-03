#file that contains general functions and variables used for portfolios
from decimal import Decimal
import json;

#I know, global variable bad, but it's a constant,ok
global DECIMAL_FORMAT
DECIMAL_FORMAT = Decimal('0.01')

def getPortfolioDict() -> dict:
    with open('portfolio.json','r') as portfolio_json:
        portfolio_dict:dict = json.load(portfolio_json)
        portfolio_json.close()
        return portfolio_dict

def writePortfolio(portfolio_dict:dict):
    with open('portfolio.json','w') as portfolio_json:
        json.dump(portfolio_dict,portfolio_json)
        portfolio_json.close()
        return 1