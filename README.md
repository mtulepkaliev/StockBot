# StockBot
Discord bot to provide stock information

## Commands
### price
#### format:
!stock price \<Ticker\> \<args\>
#### returns:
Company name, ticker, price, day change, % day change
#### args:
##### ```-range```
returns the 52 week range and day range of the specified ticker

## Portfolio Commands
These commands are used to set up and track a user's portfolio, the user adds the stock they bought and can then use commands to view their portfolio's profit and loss among other things
### add
#### format:
!stock portfolio add \<Ticker\> \<Average Price\> \<# of Shares\>
#### function:
Adds the given number of shares at the given average price for given ticker to the user's portfolio tracker
#### Note:
If the user already has shares for a given ticker, the added ones will be combined with the existing ones and the average price automatically adjusted

### show
#### format:
!stock portfolio show @\<USER\>(optional)
#### function:
Shows the given user's portfolio, shows the sender's portfolio if no user is specified

### remove
Coming soon

### change
Coming soon

### pl(Profit/Loss)
Coming soon

## How to use
Open '.env_example', insert your discord bot API key and rename to '.env'
Run stockbot.py

## Dependencies
### Python 3.10

**Python Site:** https://www.python.org/downloads/

### python-dotenv
**Project Page:** https://pypi.org/project/python-dotenv/
**Installation:** ```pip install python-dotenv```

### yfinance
**Project Page:** https://github.com/ranaroussi/yfinance
**Installation:** ```pip install yfinance```

### nextcord
**Project Page:** https://github.com/nextcord/nextcord
**Installation:** ```pip install nextcord```

## Sources
https://realpython.com/how-to-make-a-discord-bot-python/#what-is-discord

https://www.toptal.com/developers/gitignore

https://cog-creators.github.io/discord-embed-sandbox/

https://clearbit.com/logo

https://dashboard.clearbit.com/docs?javascript#logo-api