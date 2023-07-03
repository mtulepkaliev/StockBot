# Development Notes

## Current Issues

### Output formatiing
For p/l and other commands, the output is very confusin, need to find better way to display it.

### Command line arguments parsing
Need to refactor the code for command line parsing as it is clogging up the main function and also code is repeated in several points


## Potential Features

### argparses error handling
Passibly inherit argparser to that we dont have to constantly except system exit when running a parse, possibly more useful error messages too

## reduced latency for portfolio pl queries
Takes a lot of time ot get a full portfolio's PL due to having to query several tickers one by one. Need to look for way to possibly qeury multiple at once.

### imolement automated testing for the code
Need to find out how to call the discord function triggers without having to manually send messages