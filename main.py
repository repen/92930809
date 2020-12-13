import configparser, time, os, hmac, hashlib, requests
from tools import log as lo, get_signature
from datetime import datetime
from urllib.parse import urlencode


def get_timestamp():
    # 1603616154651
    # 1508396497000
    return int(time.time() * 1000)

config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
NAME = args['name']
TIMEOUT  = float( args['timeout'] )
LEVERAGE = int(args['leverage'])

log = lo( NAME, "main.log")

KEY = 'HL62GKHyIbXZraG4IB'
SECRET = 'NUR8Z7c5EtEDiPBz05dr6KayMrvlW8NljDhD'
BASE_URL = 'https://api.bybit.com' # production base url

def generate_sign():
    secret = SECRET
    params = {}
    params['api_key'] = KEY
    params['leverage'] = 100
    params['symbol'] = "BTCUSD"
    params['timestamp'] = str(get_timestamp())
    return get_signature(secret, params)


# curl https://api.bybit.com/user/leverage/save \
# -H "Content-Type: application/json" \
# -d '{"api_key":"{api_key}","symbol":"BTCUSD","leverage":14,"timestamp":{timestamp},"sign":"{sign}"}'


def get_leverage():

    params = {}
    params['api_key'] = KEY
    params['timestamp'] = str( get_timestamp() )

    url = BASE_URL + "/user/leverage"

    params["sign"] = get_signature(SECRET, params)

    query_string = urlencode(params, True)
    response = requests.get( url + "?"+ query_string )

    data = response.json()

    # print(url + "?"+query_string)

    # import pdb;pdb.set_trace()
    log.info("Get leverage = %s" % data["result"]["BTCUSD"])
    return data["result"]["BTCUSD"]["leverage"]

# curl https://api.bybit.com/user/leverage/save \
# -H "Content-Type: application/json" \
# -d '{"api_key":"{api_key}","symbol":"BTCUSD","leverage":14,"timestamp":{timestamp},"sign":"{sign}"}'

def set_leverage(number):
    headers = {"Content-Type": "application/json"}

    params = {}
    params['api_key'] = KEY
    params['symbol'] = "BTCUSD"
    params['timestamp'] = str(get_timestamp())
    params['leverage'] = str(number)
    params['sign'] = get_signature(SECRET, params)

    url = BASE_URL + "/user/leverage/save"
    response = requests.post( url, json=params, headers=headers )
    log.info("Set leverage = %s" % response.text)


def get_data():
    leverage = get_leverage()
    if leverage != LEVERAGE:
        set_leverage( 53 )


def _main():
    data = get_data()

def main():
    _main()

def work():
    while True:
        try:
            main()
            log.info("======= Sleep {} =======".format(TIMEOUT))
            time.sleep( TIMEOUT )
        except Exception as Er:
            # log.error("Error connect or work script {}. Wait 5 sec".format( Er ), exc_info=True)
            log.error("Error connect or work script {}. Wait 5 sec".format( Er ) )
            time.sleep(5)


def test():
    set_leverage(53)
    res = get_leverage()
    print(res)

if __name__ == '__main__':
    # test()
    # main()
    work()