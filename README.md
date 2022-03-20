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
## How to use
Open '.env_example', insert your discord bot API key and rename to '.env'

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