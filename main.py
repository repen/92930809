import configparser, time
from tools import log as lo
from tools import Info
from okex.futures_api import FutureAPI
from collections import namedtuple

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
FILEINFO  = args['file_info']
LEVERAGE  = float( args['leverage'] )
POLL_TIMEOUT  = float( args['poll_timeout'] )

log = lo( NAME, "main.log")

KEY = '0bed7e7b-cf4e-41b3-aeb3-565166d62166' # api_key
SECRET = '297991E27E2274F242F0BD54D33A4DDC' # secret key
PASSPHARSE = 'qwertyuiop' #Пароль для api

futureAPI = FutureAPI(KEY, SECRET, PASSPHARSE, False)

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

def set_leverage(number):
    result = futureAPI.set_leverage("BTC-USD", number)
    log.info("Set: leverage = {}".format(result))

def set_order(params):
    result = futureAPI.take_order(**params)
    log.info("Set order: %s" % params)

def get_avgEntryPrice():
    pass

def getTicker():
    result_list  = futureAPI.get_ticker()
    BTCUSD201225 = list( filter( lambda x: x['instrument_id'] == "BTC-USD-201225", result_list) )[0]
    ticker = namedtuple("Ticker", ["best_ask", "best_bid"])
    log.info("Get ticker: %s" % str(ticker))
    return ticker(best_ask=float( BTCUSD201225["best_ask"] ), best_bid=float(BTCUSD201225["best_bid"]))
    # import pdb;pdb.set_trace()

def get_leverage():
    result = futureAPI.get_leverage("BTC-USD")
    log.info("Get: leverage = {}".format( result ))
    return float(result['leverage'])



def get_posisiton():
    result = futureAPI.get_specific_position("BTC-USD-201225")
    long_qty = int( result["holding"][0]["long_qty"] )
    short_qty = int( result["holding"][0]["short_qty"] )
    long_avg_cost = float( result["holding"][0]["long_avg_cost"] )
    short_avg_cost = float( result["holding"][0]["short_avg_cost"] )
    position = namedtuple("Position", ["long_qty", "short_qty", "long_avg_cost", "short_avg_cost"])
    obj = position(long_qty, short_qty, long_avg_cost, short_avg_cost)
    log.info("Get position: {}".format(obj))
    # import pdb;pdb.set_trace()
    return obj


def script():
    position = get_posisiton()

    if position.long_qty != 0 or position.short_qty != 0:
        log.info("Position: %s. Sleep and return" % str(position) )
        time.sleep(TIMEOUT01)
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
        set_leverage(50)
        log.info("Set leverage 50")

    Fnum = info.get_num()

    if s1 > 0 or s2 > 0:
        log.info("Branch askPrice (signal1 > 0 or signal2 > 0)")
        leftPrice = getTicker().best_ask

        size   = int(leftPrice * Fnum * 47)

        set_order({
            "instrument_id" : "BTC-USD-201225",
            "size" : str(size),
            "type" : "1",
            "order_type" : "4",
            "price":None
        })


        long_avg_cost = get_posisiton().long_avg_cost
        price = int(long_avg_cost + (long_avg_cost * 0.045))
 

        set_order({
            "instrument_id" : "BTC-USD-201225",
            "size" : str(size),
            "type" : "3",
            "order_type" : "0",
            "price": price
        })

        info.add_plus()
        info.save()
        return


    if s1 < 0 or s2 < 0:
        log.info("Branch bidPrice (signal1 < 0 or signal2 < 0)")
        rightPrice = getTicker().best_bid
        size = int(rightPrice * Fnum * 48)

        set_order({
            "instrument_id" : "BTC-USD-201225",
            "size" : str(size),
            "type" : "2",
            "order_type" : "4",
            "price": None
        })

        short_avg_cost = get_posisiton().short_avg_cost
        price = int(short_avg_cost - (short_avg_cost * 0.057))
        
        set_order({
            "instrument_id" : "BTC-USD-201225",
            "size" : str(size),
            "type" : "4",
            "order_type" : "0",
            "price": price
        })

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
    script()
    # getTicker()

if __name__ == '__main__':
    # test()
    # pass
    # main()
    work()