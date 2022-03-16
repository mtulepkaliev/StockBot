
import os
import nextcord
import yfinance as yf
from dotenv import load_dotenv

from yfincode import getPriceOutput

#loads dotenv for KEYS
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')



class MyClient(nextcord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self,message):
        if(str(message.content).startswith('!stockbot ')):
            channel = message.channel
            #extract the part of the messafe after '!stockbot'
            command_text = str(message.content)[10:len(str(message.content))]
            command_text = command_text.strip()

            print("Command Received:" + command_text)

            #price command
            if(command_text.startswith('price ')):

                #extract the ticekr
                ticker_text = command_text[6:len(command_text)]
                print('Ticker Requested:' + ticker_text)
                try:
                    ticker = yf.Ticker(ticker_text)
                    ticker_info = ticker.info
                    print('Info received on ' + ticker_text)
                    if(str(ticker_info['regularMarketPrice']) == 'None'):
                        raise Exception("INVALID_TICKER_ERROR")
                    else:
                        price = str(ticker_info['regularMarketPrice'])
                except Exception as e:
                    await channel.send(content=e)
                    return
                
                await channel.send(content=getPriceOutput(ticker_text,ticker_info['shortName'],price,ticker_info['open']))







            

client = MyClient()
client.run(DISCORD_TOKEN)