# Development Notes

## Current Issues

### argument parsing
#### Invalid Ticker
Entering an invalid ticker causes crash in ticker [isValidTicker](yfincode.py#82) does not catch error, i suspect this comes from recent yfinance changes, need to change it so it catches the error

### Displaying/Calculating stock prices for penny stocks/low value coins
For stocks and coins that go beyond 2 decimal places, it is truncated, this becomes and issue for coins like SHIB-USD because it conisders the value to be 0 when running calculations <br/>
The issue with calculations might be able to be fixed by not quantizing decimal values until they need to be displayed but figuring out how many values to be dispalyed <br/>
will be a bigger issue
