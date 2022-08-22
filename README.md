# StockBot
Discord bot to provide stock information<br />
Written in python with SQLite

## Commands
### price
#### format:
!stock price \<Ticker\> \<args\>
#### returns:
Company name, ticker, price, day change, % day change
#### args:
```-range``` <br />
returns the 52 week range and day range of the specified ticker

## Portfolio Commands
These commands are used to set up and track a user's portfolio, the user adds the stock they bought and can then use commands to view their portfolio's profit and loss among other things
### add
#### format:
!stock portfolio add \<Ticker\> \<Average Price\> \<# of Shares\>
#### function:
Adds the given number of shares at the given average price for given ticker to the user's portfolio tracker

### show
#### format:
!stock portfolio show @\<USER\>(optional) \<args\>(optional)
#### function:
Shows the given user's portfolio, shows the sender's portfolio if no user is specified

#### display args:
```-net``` <br />
Shows the total cost basis for the given user <br />
```-brief``` <br />
(default) Shows the average price, # of shares and cost basis of each ticker that the user holds <br />
```-full``` <br />
Shows each position that the user hold not grouping by ticker

### remove
#### format:
!stock portfolio remove \<position #\>
#### function:
Removes the given position from the user's portfolio
#### Notes:
You can get the position # from the show command with the -full argument

### change
Coming soon

### pl(Profit/Loss)
Coming soon

## How to use
Open '.env_example', insert your discord bot API key and rename to '.env' </br>
Rename 'portfolio_ex.db' to 'portfolio.db'</br>
Run stockbot.py </br>
**Grant all priveleged intents to the bot**</br>

## Dependencies
### Python 3.10

**Python Site:** https://www.python.org/downloads/

### python-dotenv
**Project Page:** https://pypi.org/project/python-dotenv/ <br />
**Installation:** ```pip install python-dotenv```

### yfinance
**Project Page:** https://github.com/ranaroussi/yfinance <br />
**Installation:** ```pip install yfinance```

### nextcord
**Project Page:** https://github.com/nextcord/nextcord <br />
**Installation:** ```pip install nextcord```

## Sources
https://realpython.com/how-to-make-a-discord-bot-python/#what-is-discord

https://www.toptal.com/developers/gitignore

https://cog-creators.github.io/discord-embed-sandbox/

https://clearbit.com/logo

https://dashboard.clearbit.com/docs?javascript#logo-api