import configparser, time
from tools import log as lo
from tools import Info
import bybit

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

KEY = ''
SECRET = ''
BASE_URL = 'https://api.bybit.com' # production base url


client  = bybit.bybit(test=False, api_key=KEY, api_secret=SECRET)

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
    data = client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="{}".format(number)).result()
    log.info( "set_leverage: %d" % number )
    return data

def set_order(order):
    data = client.Order.Order_new(**order).result()
    log.info( "Set_order: {}".format( order ) )

def get_avgEntryPrice():
    data=client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    log.info( "get_avgEntryPrice: %s" % data[0]["result"]["entry_price"] )
    return float( data[0]["result"]["entry_price"] )

def getOrderBook(side):
    # Уточнить какие значения нужны. Возвращается список прайсов.
    data = client.Market.Market_orderbook(symbol="BTCUSD").result()
    select = list( filter( lambda x: x["side"] == side , data[0]["result"]) )
    log.info( "getOrderBook %s: %s" % ( side, select ) )
    return float( select[0]["price"] )

def get_leverage():
    data = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    log.info( "get_leverage: %s" % data[0]["result"]["leverage"] )
    return int( data[0]["result"]["leverage"] )


def get_Size():
    data = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    log.info( "get_Size: %s" % data[0]["result"]["size"] )
    return int(data[0]["result"]["size"])


def script():
    Size = get_Size()
    
    # import pdb;pdb.set_trace()
    log.info( "Size = {}".format( Size ) )
    if Size != 0:
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
        set_leverage(50)
        log.info("Set leverage 50")

    Fnum = info.get_num()

    if s1 > 0 or s2 > 0:
        log.info("Branch askPrice (signal1 > 0 or signal2 > 0)")
        leftPrice   = getOrderBook("Sell")

        orderQty   = int(leftPrice * Fnum * 47)

        set_order({
            "side": "Buy", "symbol" : "BTCUSD", "order_type" : "Market", 
            "qty":orderQty, "time_in_force": "FillOrKill"
        })

        entry_price = get_avgEntryPrice()
        price = int(entry_price + (entry_price * 0.045))
 
        set_order({
            "side" : "Sell", "symbol" : "BTCUSD", "order_type" : "Limit", 
            "qty" : orderQty, "price":price, "time_in_force":"GoodTillCancel"
        })

        info.add_plus()
        info.save()
        return


    if s1 < 0 or s2 < 0:
        log.info("Branch bidPrice (signal1 < 0 or signal2 < 0)")
        rightPrice = getOrderBook("Buy")
        orderQty = int(rightPrice * Fnum * 48)

        set_order({
            "side": "Sell", "symbol" : "BTCUSD", "order_type" : "Market", 
            "qty":orderQty, "time_in_force": "FillOrKill"
        })

        entry_price = get_avgEntryPrice()
        price = int(entry_price - (entry_price * 0.057))
        
        set_order({
            "side" : "Buy", "symbol" : "BTCUSD", "order_type" : "Limit", 
            "qty" : orderQty, "price":price, "time_in_force":"GoodTillCancel"
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
    # getOrderBook("Buy")

if __name__ == '__main__':
    # test()
    # pass
    # main()
    work()