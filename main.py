import configparser, time
from requests.auth import AuthBase
from threading import Thread
from queue import Queue
from tools import log as lo
from custom import functions
from tools import generate_signature
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests
config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
NAME = args['name']
TIMEOUT  = float( args['timeout'] )
LEVERAGE = float( args['leverage'] )

log = lo( NAME, "main.log")

def comma(float):
    res = "{}".format( float )
    res = res.replace(".",",")
    return res

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

def get_data():

    apiKey    = "BBDLor4hAF9Aplqp62oNCK-q"
    apiSecret = "ay5rZbB_aYeMQ4R9IIbbr777oxL6CdeXVHUTcz6451hY1nX5"
    URL = "https://testnet.bitmex.com/api/v1/position?filter=%7B%22symbol%22%3A%20%22XBTUSD%22%7D"
    response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)

    log.info( "Response {} limit: {}".format( response, response.headers["X-RateLimit-Remaining"] ) )
    data = response.json()
    if not data:
        log.info("Not data")
        return
    
    data = data[0]

    if data["leverage"] == LEVERAGE:
        log.info( "Miss. leverage == {}".format( LEVERAGE ) )
        return

    url = "https://testnet.bitmex.com/api/v1/position/leverage"
    
    set_data = "symbol=XBTUSD&leverage={}".format( LEVERAGE )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    response = requests.post( url, 
        data=set_data, headers=headers, auth=APIKeyAuthWithExpires(apiKey, apiSecret), 
        timeout=2.001
    )
    
    if response.status_code == 200:
        log.info( "leverage change! before {} | after {}".format(data["leverage"], LEVERAGE ) )
    else:
        log.info( "Bad status code {}.leverage value not setting!".format( response.status_code) )
    pass
    # end



def wrapper_run(*args, **kwargs):

    queue    = args[0]
    function = args[1]
    data     = args[2]
    index    = args[3]

    start_time = time.time()
    
    res = function(data)

    end_time = time.time()
    end_time = end_time - start_time

    log.info( "Run time: {:.10f} sec for function {}".format( end_time, index ) )
    queue.put( ( res, index ) )


def _main():
    data = get_data()


def main():
    _main()

def work():
    while True:
        try:
            main()
            log.info("Sleep {}".format(TIMEOUT))
            time.sleep( TIMEOUT )
        except Exception as Er:
            # log.error("Error connect or work script {}. Wait 5 sec".format( Er ), exc_info=True)
            log.error("Error connect or work script {}. Wait 5 sec".format( Er ) )
            time.sleep(5)


def test():
    res = get_data()

if __name__ == '__main__':
    # test()
    # main()
    work()