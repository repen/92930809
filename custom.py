
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
    for row in data['bids']:
        price  = float( row['price'] )
        amount = float( row['amount'] )
        summ  += price * amount
    result = summ
    return result

functions = [ func01, func02, func03 ]

# ============= Custom function ================