import configparser, time, os, hmac, hashlib, requests
from tools import log as lo
from datetime import datetime
from urllib.parse import urlencode

config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
NAME = args['name']
TIMEOUT  = float( args['timeout'] )
LEVERAGE = int(args['leverage'])

log = lo( NAME, "main.log")

KEY = ''
SECRET = ''
BASE_URL = 'https://fapi.binance.com' # production base url

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

def get_data():

    params = {"symbol" : "BTCUSDT",}
    response01 = send_signed_request("GET",'/fapi/v2/positionRisk' , {"symbol": "BTCUSDT", "timestamp":get_timestamp()})

    data = response01
    if data:
        data = data[0]
        if int(data["leverage"]) == LEVERAGE:
            log.info( "Miss. leverage == %s" % LEVERAGE )
            return

    response02 = send_signed_request("POST",'/fapi/v1/leverage' , {
            "symbol": "BTCUSDT", 
            "timestamp":get_timestamp(),
            "leverage" : int(LEVERAGE)

    })

    log.info( "leverage change! before %s | after %s" % ( data["leverage"], LEVERAGE ) )


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