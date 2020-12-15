from tools import log as lo
from datetime import datetime
from okex.futures_api import FutureAPI
from configparser import ConfigParser
from itertools import count
import time

config = ConfigParser()
config.read('setting.conf')

args = config['site']
NAME = args['name']
TIMEOUT  = float( args['timeout'] )
LEVERAGE = int(args['leverage'])

log = lo( NAME, "main.log")


KEY = '' # api_key
SECRET = '' # secret key
PASSPHARSE = '' #Пароль для api

futureAPI = FutureAPI(KEY, SECRET, PASSPHARSE, False)


def get_timestamp():
    now = datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


def get_leverage():
    result = futureAPI.get_leverage("BTC-USD")
    log.info("Get: leverage = {}".format( result ))
    return float(result['leverage'])

def set_leverage(number):
    result = futureAPI.set_leverage("BTC-USD", number)
    log.info("Set: leverage = {}".format(result))


def _main():
    leverage = get_leverage()
    if leverage != LEVERAGE:
        set_leverage( 53 )



def main():
    _main()

def work():
    for _ in count(1):
        try:
            main()
            log.info("Sleep {}".format(TIMEOUT))
            time.sleep( TIMEOUT )
        except Exception as Er:
            # log.error("Error connect or work script {}. Wait 5 sec".format( Er ), exc_info=True)
            log.error("Error connect or work script {}. Wait 5 sec".format( Er ) )
            time.sleep(5)


def test():
    main()

if __name__ == '__main__':
    # test()
    # main()
    work()