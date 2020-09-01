
# ============= Custom function ================

def func01(data ):
    buy_rows    = list( filter( lambda x:x["side"] == "Buy", data ) )
    result = buy_rows[0]['price']
    return result

def func02(data):
    sell_rows = list( filter( lambda x:x["side"] == "Sell", data ) )
    result = sell_rows[-1]['price']
    return result

def func03(data):
    summ = 0

    buy_rows    = list( filter( lambda x:x["side"] == "Buy", data ) )
    
    first_price = float( buy_rows[0]['price']  )
    last_price  = float( buy_rows[-1]['price'] )
    
    # sell_rows = list( filter( lambda x:x["side"] == "Sell", data ) )
    # last_price = sell_rows[-1]['price']
    
    for row in buy_rows:
        price = float( row['price'] )
        size = float(  row['size'] )
        summ += price * size * (first_price + 5 + last_price)
    result = summ

    return result


functions = [ func01, func02, func03, ]

# ============= Custom function ================