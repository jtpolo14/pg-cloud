import requests

class Token:
    def __init__(self, name, address, minDivUnit):
        self.name = name # coin ticker
        self.address = address # eth address
        self.minDivUnit = minDivUnit # minimal divisible unit as described by 1inch api
    
    def convertWithMinDivUnit(self, amt):
        return amt / self.minDivUnit
    

def GetQuoteFrom1inch(fromToken, toToken):
    # construct the 1inch url with the proper parameters
    url = 'https://api.1inch.exchange/v3.0/1/quote?fromTokenAddress={0}&toTokenAddress={1}&amount={2}' \
        .format(fromToken.address, toToken.address, fromToken.minDivUnit)
    # call the 1inch api 
    rawResponse = requests.get(url).json()
    # clean up the response data so we dont have to do it later
    rawResponse['toTokenAmountCln'] = toToken.convertWithMinDivUnit(int(rawResponse['toTokenAmount']))
    
    return rawResponse

if __name__=='__main__'():
    
    tether = Token('usdt', '0xdac17f958d2ee523a2206206994597c13d831ec7', 1000000)
    wBitcoin = Token('wbtc', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', 100000000)
    response = GetQuoteFrom1inch(wBitcoin, tether)

    print(response['toTokenAmountCln'])
