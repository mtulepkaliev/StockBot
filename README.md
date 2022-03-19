# StockBot
Discord bot to provide stock information

## Commands
### price
#### format:
!stock price \<Ticker\>
#### returns:
Company name, ticker, price, day change, % day change

## How to use
Open '.env_example', insert your discord bot API key and rename to '.env'

## Notes
### Execution Time
The lag between issuing a command and receiving a response can sometimes be upwards of 20 seconds, this is due how long it takes to retrieve data from yfinance and not due to my code.
##### If you know of a way to fix this or an alternate, free API to use please let me know by opening an issue
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
