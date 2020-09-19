import configparser, time, re
from requests.auth import AuthBase
from tools import log as lo
from tools import generate_signature
import requests
config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']

#load config
NAME = args['name']
TIMEOUT01 = float( args['timeout01'] )
TIMEOUT02 = float( args['timeout02'] )
TIMEOUT03 = float( args['timeout03'] )
FILE01  = args['file01']
FILE02  = args['file02']
LEVERAGE  = float( args['leverage'] )
POLL_TIMEOUT  = float( args['poll_timeout'] )

log = lo( NAME, "main.log")

apiKey = "BBDLor4hAF9Aplqp62oNCK-q"
apiSecret = "ay5rZbB_aYeMQ4R9IIbbr777oxL6CdeXVHUTcz6451hY1nX5"

POST_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}


class APIKeyAuthWithExpires(AuthBase):

    """Attaches API Key Authentication to the given Request object. This implementation uses `expires`."""

    def __init__(self, apiKey, apiSecret):
        """Init with Key & Secret."""
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def __call__(self, r):
        """
        Called when forming a request - generates api key headers. This call uses `expires` instead of nonce.
        This way it will not collide with other processes using the same API Key if requests arrive out of order.
        For more details, see https://www.bitmex.com/app/apiKeys
        """
        # modify and return the request
        expires = int(round(time.time()) + 5)  # 5s grace period in case of clock skew
        r.headers['api-expires'] = str(expires)
        r.headers['api-key'] = self.apiKey
        r.headers['api-signature'] = generate_signature(self.apiSecret, r.method, r.url, expires, r.body or '')
        return r

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
    URL = "https://testnet.bitmex.com/api/v1/position/leverage"
    
    set_data = "symbol=XBTUSD&leverage={}".format( LEVERAGE )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    response = requests.post( URL, 
        data=set_data, headers=headers, auth=APIKeyAuthWithExpires(apiKey, apiSecret), 
        timeout=2.001
    )
    log.info( "response {}. Url: {} ".format( response, URL) )
    return response

def set_order(order_data):
    URL = "https://testnet.bitmex.com/api/v1/order"
    response  = requests.post( URL, data=order_data, headers=POST_HEADERS, 
        auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001
    )
    log.info( "response {}. Url:  {}".format( response, URL) )
    return response

def get_avgEntryPrice():
    URL = "https://testnet.bitmex.com/api/v1/position?filter=%7B%22symbol%22%3A%20%22XBTUSD%22%7D&columns=%5B%22avgEntryPrice%22%5D"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    data = response.json()
    avgEntryPrice = data[0]['avgEntryPrice']

    return avgEntryPrice

def get_askPrice():
    URL = "https://testnet.bitmex.com/api/v1/instrument?symbol=XBT%3Aperpetual&columns=%5B%22askPrice%22%5D&reverse=false"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    data = response.json()
    askPrice = data[0]['askPrice']
    return askPrice

def get_bidPrice():
    URL = "https://testnet.bitmex.com/api/v1/instrument?symbol=XBT%3Aperpetual&columns=%5B%22bidPrice%22%5D&reverse=false"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    data = response.json()
    bidPrice = data[0]['bidPrice']
    return bidPrice

def get_leverage():
    URL = "https://testnet.bitmex.com/api/v1/position?filter=%7B%22symbol%22%3A%20%22XBTUSD%22%7D&columns=%5B%22leverage%22%5D"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    data = response.json()
    leverage = data[0]['leverage']
    return leverage

def get_currentQty():
    URL = "https://testnet.bitmex.com/api/v1/position?filter=%7B%22symbol%22%3A%20%22XBTUSD%22%7D&columns=%5B%22currentQty%22%5D"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    log.info( "response {} limit: {}".format( response, response.headers["X-RateLimit-Remaining"] ) )
    data = response.json()
    currentQty = data[0]['currentQty']
    return currentQty

def get_position():
    URL = "https://testnet.bitmex.com/api/v1/execution?symbol=XBT%3Aperpetual&columns=%5B%22text%22%5D&count=1&reverse=true"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)
    log.info( "response {}. Url: {}".format( response, URL) )
    data = response.json()
    text =  data[0]['text']
    return text

def script():
    currentQty = get_currentQty()
    
    # import pdb;pdb.set_trace()
    log.info( "currentQty = {}".format( currentQty ) )
    if currentQty != 0:
        time.sleep( TIMEOUT01 )
        log.info( "Sleep: {}".format( TIMEOUT01 ) )
        return

    # remove
    # log.info( "Sleep: {}".format( TIMEOUT02 ) )
    # time.sleep( TIMEOUT02 )
    # ==========
    
    #new block
    position = get_position()
    log.info( "Get_position: {}".format( position ) )
    if position == "Liquidation":
        log.info( "Sleep: {}".format( TIMEOUT03 ) )
        time.sleep(TIMEOUT03)
    else:
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


    if s1 > 0 or s2 > 0:
        log.info("Branch askPrice (signal1 > 0 or signal2 > 0)")
        askPrice   = get_askPrice()
        orderQty   = int(askPrice * 0.0001 * 47)
        order_data = "symbol=XBTUSD&side=Buy&orderQty={}&ordType=Market".format( orderQty )

        set_order( order_data )

        avgEntryPrice = get_avgEntryPrice()
        price = int(avgEntryPrice + (avgEntryPrice * 0.045))
        order_data = "symbol=XBTUSD&price={}&execInst=Close".format( price )
        
        set_order( order_data )
        return


    if s1 < 0 or s2 < 0:
        log.info("Branch bidPrice (signal1 < 0 or signal2 < 0)")
        bidPrice = get_bidPrice()
        orderQty = int(bidPrice * 0.0002 * 48)
        order_data = "symbol=XBTUSD&side=Sell&orderQty={}&ordType=Market".format( orderQty )
        
        set_order( order_data )

        avgEntryPrice = get_avgEntryPrice()
        price = int(avgEntryPrice - (avgEntryPrice * 0.057))
        order_data = "symbol=XBTUSD&price={}&execInst=Close".format( price )
        
        set_order( order_data )
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
    script()

if __name__ == '__main__':
    # test()
    # pass
    # main()
    work()