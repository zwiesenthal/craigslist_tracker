import requests

# future additions:
#    min price
#    other parameters
#    location

PRICE_STRING = "$"
NAME_STRING = ""
BASE = 10

def toInt(string):
    out = 0
    for char in string:
        if '0' <= char <= '9':
            out *= BASE
            out += int(char)   
    return out
    

# return (nextIdx, price)
def findPrice(resp, idx):
    try:
        idx = resp.index(PRICE_STRING, idx)
        priceIdxStart = idx + len(PRICE_STRING)
        priceIdxEnd = resp.index("<", priceIdxStart)
        priceString = resp[priceIdxStart : priceIdxEnd]
        priceInt = toInt(priceString)
        return (priceIdxEnd, priceInt)
    except ValueError:
        return (-1, -1)


def getPrices(resp):
    idx = 0
    prices = []

    while idx != -1:
        idx, price = findPrice(resp, idx)
        prices.append(price)

    return prices

def cleanPrices(prices, minPrice = 10):
    # remove back to back duplicates
    out = []
    for i, price in enumerate(prices):
        # skip every other price that is the same as the last, removes back to back same prices for the same entry
        if (i % 2 == 0 or out == [] or price != out[-1]) and price >= minPrice: 
            out.append(price)
    return out
    
    

if __name__ == "__main__":

    resp = requests.get('https://orangecounty.craigslist.org/d/for-sale/search/sss?query=bikes&sort=rel')

    resp = str(resp.content)

    prices = getPrices(resp)
    prices = cleanPrices(prices)

    avg = sum(prices) / len(prices)

    print("Average Price: $" + str(avg))
    print(prices)
    

        
    
    

