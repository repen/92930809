
# ============= Custom function ================

def func01(data ):
    first_price_bids = data['result']['XETHZEUR']['bids'][0][0]
    return first_price_bids

def func02(data):
    first_price_asks = data['result']['XETHZEUR']['asks'][0][0]
    return first_price_asks

def func03(data):
    summ = 0
    first_price_bids = float( data['result']['XETHZEUR']['bids'][0][0] )
    for row in data['result']['XETHZEUR']['bids']:
        price = float( row[0] )
        size = float( row[1] )
        summ += price * size * (first_price_bids + 5)
    result = summ
    return result

functions = [ func01, func02, func03]

# ============= Custom function ================