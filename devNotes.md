# Development Notes

## Current Issues


### Displaying/Calculating stock prices for penny stocks/low value coins
For stocks and coins that go beyond 2 decimal places, it is truncated, this becomes and issue for coins like SHIB-USD because it conisders the value to be 0 when running calculations <br/>
The issue with calculations might be able to be fixed by not quantizing decimal values until they need to be displayed ~~but figuring out how many values to be dispalyed <br/>
will be a bigger issue~~ <br/>
the json data returned from yfinance includes a pricehint field that can be used to determine how many decimal places to display, need to figure out how to store this, possibly in database, might store the pricehint value as '2' or maybe as '0.01' and then use that to determine how many decimal places to display, dont want to have to do those extra calculations every time we get ticker info though
