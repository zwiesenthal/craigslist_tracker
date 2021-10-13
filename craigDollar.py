import requests
from datetime import datetime

# convert string to an int, excluding all non numeric characters
def toInt(string):
    BASE = 10

    out = 0
    for char in string:
        if '0' <= char <= '9':
            out *= BASE
            out += int(char)   
    return out
    
# return (nextIdx, price)
def findPrice(resp, idx):
    PRICE_STRING = "$"

    try:
        idx = resp.index(PRICE_STRING, idx)
        priceIdxStart = idx + len(PRICE_STRING)
        priceIdxEnd = resp.index("<", priceIdxStart)
        priceString = resp[priceIdxStart : priceIdxEnd]
        priceInt = toInt(priceString)
        return (priceIdxEnd, priceInt)
    except ValueError:
        return (-1, -1)


# return a list of all numbers directly after dollar signs
def getPrices(resp):
    idx = 0
    prices = []

    while idx != -1:
        idx, price = findPrice(resp, idx)
        prices.append(price)

    return prices

# remove back to back duplicates and eliminate price outliers
def cleanPrices(prices, minPrice = 10, maxPrice = 15000):
    out = []
    for i, price in enumerate(prices):
        # skip every other price that is the same as the last, removes back to back same prices for the same entry
        if i % 2 == 0 or not out or price != out[-1]:
            if minPrice <= price <= maxPrice:
                out.append(price)
    return out

def median(prices):
    if not prices:
        return -1
    return sorted(prices)[len(prices)//2]

# get the total number of items posted in the category for the day
def totalCount(resp):
    TOTAL_COUNT = '"totalcount">'

    idx = resp.index(TOTAL_COUNT)
    cntStart = idx + len(TOTAL_COUNT)
    cntEnd = resp.index('<', cntStart)
    dailyPosted = toInt(resp[cntStart:cntEnd])
    return dailyPosted
    
def writePricesToFile(fileName, itemCount, mean, median):
    file = open(fileName, 'a')
    file.write("{}, {}, {}, {}".format(datetime.today(), itemCount, mean, median))
    file.close()

def postPrices(priceArr, area, category, flags):
    url = "http://127.0.0.1:5000/bike"

    response = requests.post(url, data =
        {"prices" : priceArr, 
        "date": datetime.today(),
        "area": area,
        "category": category,
        "flags": flags
        })

    print(response)

def main():
    AREA="orangecounty"
    CATEGORY="bicycles"
    FLAGS="postedToday=1"
    
    # get html of bicyces in orange county posted today
    queryString = f"https://{AREA}.craigslist.org/d/{CATEGORY}/search/bia?{FLAGS}"
    resp = requests.get(queryString)

    resp = str(resp.content)

    # generate prices and total item count from response
    all_prices = getPrices(resp)
    prices = cleanPrices(all_prices)
    itemCount = totalCount(resp)

    mean = sum(prices) / len(prices)
    medianVal = median(prices)

    fileName = AREA + '_' + CATEGORY + '.csv'
    writePricesToFile(fileName=fileName, itemCount=itemCount, mean=mean, median=medianVal)
    postPrices(priceArr=prices, area=AREA, category=CATEGORY, flags=FLAGS)


if __name__ == "__main__":
   main()
    