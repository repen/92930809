import configparser
import requests, time
from multiprocessing import Process, SimpleQueue
from tools import log as lo
from custom import functions


log = lo("Main", "main.log")
config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
URL  = args['url']
PATH = args['result_path']
TIMEOUT = int( args['timeout'] )

def comma(float):
    res = "{}".format( float )
    res = res.replace(".",",")
    return res

def get_data():
    response = requests.get( URL )
    if response.status_code == 200:
        return response.json()
    raise ValueError

def init_wrapper(*args, **kwargs):
    queue    = args[0]
    function = args[1]
    data = args[2]
    index  = args[3]
    def wrapper(*args, **kwargs):

        start_time = time.time()
        
        res = function(data)

        end_time = time.time()
        end_time = end_time - start_time

        log.info( "Run time: {:.10f} sec for function {}".format( end_time, index ) )
        queue.put( ( res, index ) )
    return wrapper

def save( data ):
    data = sorted( data, key=lambda x : x[1])
    res = [comma(x[0]) for x in data]
    string = ";".join( res )
    with open(PATH, "w", encoding="utf8") as f:
        f.write( string )
    log.info( "Save {} in {}".format( string, PATH ) )


def _main():
    q = SimpleQueue()
    data = get_data()
    objs = []
    for e, func in enumerate( functions , start=1):
        objs.append( init_wrapper( q, func, data, e ) )
    processes = [ Process(target=x) for x in objs ]
    [x.start() for x in processes]
    [x.join() for x in processes]
    results = []
    while True:
        items = q.get()
        results.append( items )
        if q.empty():
            break
    save( results )


def work():
    while True:
        try:
            main()
        except Exception as Er:
            log.error("Error {}".format(str(Er)) ,exc_info=True)
        finally:
            log.info("Sleep: {}".format(TIMEOUT))
            time.sleep( TIMEOUT )


def main():
    _main()

if __name__ == '__main__':
    main()
    # work()