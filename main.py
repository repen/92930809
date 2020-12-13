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

KEY = 'O0WIAYP8jc4tLZ03dc'
SECRET = 'MsoezA2ruNnEGoaAQNHVXAQxL2GFLcHhLtbl'
BASE_URL = 'https://api.bybit.com' # production base url

def get_timestamp():
    # 1603616154651
    # 1508396497000
    return int(time.time() * 1000)

# curl https://api.bybit.com/user/leverage/save \
# -H "Content-Type: application/json" \
# -d '{"api_key":"{api_key}","symbol":"BTCUSD","leverage":14,"timestamp":{timestamp},"sign":"{sign}"}'


def get_leverage():
    # curl "https://api.bybit.com/user/leverage?api_key={api_key}&timestamp={timestamp}&sign={sign}"
    headers = {"Content-Type": "application/json"}
    url = BASE_URL + "/user/leverage"
    payload = {
        "api_key" : KEY,
        "sign" : SECRET,
        "timestamp" : get_timestamp(),
    }
    query_string = urlencode(payload, True)
    response = requests.get( url + "?"+query_string )
    print(url + "?"+query_string)

    import pdb;pdb.set_trace()
    pass

def get_data():

    response01 = send_signed_request("GET",'/dapi/v1/positionRisk' , 
        {"pair": "BTCUSD"}
    )
    
    data_list = response01
    data_list = list( filter( lambda x : x['symbol'] == "BTCUSD_PERP", data_list ) )

    # import pdb;pdb.set_trace()
    
    data = data_list[0]
    if int(data["leverage"]) == LEVERAGE:
        log.info( "Miss. leverage == %s" % LEVERAGE ) 
        return

    response02 = send_signed_request("POST",'/dapi/v1/leverage' , {
            "symbol": "BTCUSD_PERP", 
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
    res = get_leverage()
    print(res)

if __name__ == '__main__':
    test()
    # main()
    # work()