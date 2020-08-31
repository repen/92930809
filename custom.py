
# ============= Custom function ================

def func01(data ):
    accum = []
    for row in data['bids']:
        price = float( row['price'] )
        accum.append( price )
    result = max( accum )
    return result

def func02(data):
    accum = []
    for row in data['asks']:
        price = float( row['price'] )
        accum.append( price )
    result = min( accum )
    return result

def func03(data):
    summ = 0
    first_price = float( data['bids'][0]['price'] )
    for row in data['bids']:
        price  = float( row['price'] )
        amount = float( row['amount'] )
        summ += price * amount * (first_price + 5)
    result = summ
    return result

def func04(data):
    first_price = data['bids'][0]['price']
    return first_price



def func05(data):
    summ = 0
    first_price = float( data['bids'][0]['price'] )
    for row in data['bids']:
        price  = float( row['price'] )
        amount = float( row['amount'] )
        summ += price * amount * (first_price + 5)
    result = summ
    return result


def func10(data):
    summ = 0
    first_price = float( data['bids'][0]['price'] )
    for row in data['bids']:
        s = 100 ** 10000
        price  = float( row['price'] )
        amount = float( row['amount'] )
        summ += price * amount * (first_price + 5)
        s = s - 2000000000000000000
    result = summ
    return result


functions = [ func10, func10, func10, func10, func10, func10, func10, func10, func10, func10, func10]
# functions = [ func10, func10, func10]

# ============= Custom function ================