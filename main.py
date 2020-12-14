import configparser, time, os, hmac, hashlib, requests
from tools import log as lo, Info
from datetime import datetime
from urllib.parse import urlencode

config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']

#load config
NAME = args['name']
TIMEOUT01 = float( args['timeout01'] )
TIMEOUT02 = float( args['timeout02'] )
FILE01  = args['file01']
FILE02  = args['file02']
FILEINFO  = args['file_info']
LEVERAGE  = float( args['leverage'] )
POLL_TIMEOUT  = float( args['poll_timeout'] )

log = lo( NAME, "main.log")

KEY = ''
SECRET = ''
BASE_URL = 'https://dapi.binance.com' # production base url


def get_timestamp():
    # 1603616154651
    # 1508396497000
    return int(time.time() * 1000)

def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    log.info("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    log.info("{}".format(url))
    response = dispatch_request('GET')(url=url)
    return response.json()


def get_signal(path):
    while True:
        with open(path) as f:
            data = f.read()
        data = data.strip()
        try:
            result = int(data)
            log.info("File: {}. Value: {}".format(path, result))
            break
        except ValueError:
            log.info("file {} value = {} error. not number.".format(path, data))
            log.info("file {} reopen".format(path))
            time.sleep(0.1)
    return result

def set_leverage():
    response = send_signed_request("POST",'/dapi/v1/leverage' , {
            "symbol": "BTCUSD_PERP", 
            "leverage" : int(LEVERAGE)

    })

def set_order_left(quantity):
    response = send_signed_request("POST",'/dapi/v1/order' , {
            "symbol": "BTCUSD_PERP", 
            "side": "BUY", 
            "type": "MARKET", 
            "quantity": quantity, 

    })
    log.info("set_order_left: %s" % response )

def set_order_right(quantity):
    response = send_signed_request("POST",'/dapi/v1/order' , {
            "symbol": "BTCUSD_PERP", 
            "side": "SELL", 
            "type": "MARKET", 
            "quantity": quantity,

    })
    log.info("set_order_right: %s" % response )

def set_order_left2(price, quantity):
    response = send_signed_request("POST",'/dapi/v1/order' , {
            "symbol": "BTCUSD_PERP",
            "side": "SELL",
            "type": "LIMIT",
            "price": price,
            "quantity": quantity,

    })
    log.info("set_order_left2: %s" % response )

def set_order_right2(price, quantity ):
    response = send_signed_request("POST",'/dapi/v1/order' , {
            "symbol": "BTCUSD_PERP",
            "side": "BUY",
            "type": "LIMIT",
            "price": price,
            "quantity": quantity,

    })
    log.info("set_order_right2: %s" % response )


def get_avgEntryPrice():
    response = send_signed_request("GET",'/dapi/v1/positionRisk' , 
        {"pair": "BTCUSD"}
    )

    result = list( filter(lambda x : x['symbol'] == "BTCUSD_PERP", response) )
    avgEntryPrice = result[0]["entryPrice"]
    return float(avgEntryPrice)

def get_leverage():
    response = send_signed_request("GET",'/dapi/v1/positionRisk' , 
        {"pair": "BTCUSD"}
    )

    if not response:
        return -1

    result = list( filter(lambda x : x['symbol'] == "BTCUSD_PERP", response) )

    leverage = result[0]['leverage']
    return int(leverage)

def get_positionAmt():
    response = send_signed_request("GET",'/dapi/v1/positionRisk' , 
        {"pair": "BTCUSD"}
    )

    result = list( filter(lambda x : x['symbol'] == "BTCUSD_PERP", response) )
    positionAmt = result[0]["positionAmt"]
    return int(positionAmt)

def get_price(name):
    '''
    Получение значений по полям askPrice и bidPrice

    Параметры:
        name (str): Ожидается строка со значением askPrice или bidPrice
    
    Вернуть:
        float: число в типе float

    '''

    response = send_signed_request("GET",'/dapi/v1/ticker/bookTicker' , 
        {"symbol": "BTCUSD_PERP"}
    )


    return float(response[0][name])

def script():
    positionAmt = get_positionAmt()
    
    # import pdb;pdb.set_trace()
    log.info( "positionAmt = {}".format( positionAmt ) )
    if positionAmt != 0:
        time.sleep( TIMEOUT01 )
        log.info( "Sleep: {}".format( TIMEOUT01 ) )
        return


    info = Info( FILEINFO )
    log.info("Load file %s \n data: %s", FILEINFO, info)
    
    if info.length_plus() == 5:
        info.clear_plus()
        info.save()

    log.info( "Sleep: {}".format( TIMEOUT02 ) )
    time.sleep(TIMEOUT02)
    # ==========


    
    # читать файлы с сигналами N 0 -N
    while True:
        s1 = get_signal(FILE01)
        s2 = get_signal(FILE02)
        if s1 > 0 or s1 < 0 or s2 > 0 or s2 < 0:
            #прекратить чтение файлов
            break
        #задержка перед чтением
        time.sleep( POLL_TIMEOUT )

    log.info( "signal1: {} | signal2: {}".format( s1,s2 ) )
    
    #проверить плечо
    leverage = get_leverage()    
    if leverage != 50:
        set_leverage()
        log.info("Set leverage 50")

    Fnum = info.get_num()
    log.info("Fnum: {}".format( Fnum ) )

    if s1 > 0 or s2 > 0:
        log.info("Branch (signal1 > 0 or signal2 > 0)")

        askPrice = get_price("askPrice")

        quantity = int( askPrice * Fnum * 47 )
        set_order_left( quantity )

        entryPrice = get_avgEntryPrice()
        price = int(entryPrice + (entryPrice * 0.045))
        set_order_left2( price, quantity )
        
        info.add_plus()
        info.save()
        return


    if s1 < 0 or s2 < 0:
        log.info("Branch (signal1 < 0 or signal2 < 0)")

        bidPrice = get_price("bidPrice")
        quantity = int(bidPrice * Fnum * 48)

        set_order_right( quantity )

        entryPrice = get_avgEntryPrice()
        price = int(entryPrice - (entryPrice * 0.045))
        set_order_right2( price, quantity )
        
        info.add_plus()
        info.save()
        return


    
    # import pdb;pdb.set_trace()


def _main():
    script()

def main():
    _main()

def work():
    while True:
        try:
            main()
            log.info("========End========")
        except Exception as Er:
            log.error("Error connect or work script {}. Wait 5 sec".format( Er ), exc_info=True)
            # log.error("Error connect or work script {}. Wait 5 sec".format( Er ) )
            time.sleep(5)
            log.info("========End========")


def test():
    pass

if __name__ == '__main__':
    # test()
    # pass
    # main()
    work()