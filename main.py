import configparser
import requests, time
from queue import Queue
from tools import log as lo
from custom import functions
from concurrent.futures import ThreadPoolExecutor
from functools import partial


config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
URL  = args['url']
NAME  = args['name']
PATH = args['result_path']
TIMEOUT = float( args['timeout'] )
WORKER = int( args['worker'] )

log = lo(NAME, "main.log")

def comma(float):
    res = "{}".format( float )
    res = res.replace(".",",")
    return res

def get_data():
    try:
        response = requests.get( URL, timeout=2.001 )
        return response.json()
    except Exception as e:
        log.info("Error connect {}. Wait 5 sec".format( e ))
        time.sleep(5)
        return get_data()


def wrapper_run(*args, **kwargs):

    queue    = args[0]
    function = args[1]
    data = args[2]
    index  = args[3]

    start_time = time.time()
    
    res = function(data)

    end_time = time.time()
    end_time = end_time - start_time

    log.info( "Run time: {:.10f} sec for function {}".format( end_time, index ) )
    queue.put( ( res, index ) )




def save( data ):
    data = sorted( data, key=lambda x : x[1])
    res = [comma(x[0]) for x in data]
    string = ";".join( res )
    with open(PATH, "w", encoding="utf8") as f:
        f.write( string )
    log.info( "Save {} in {}".format( string, PATH ) )

def call(f):
    f()

def _main():
    q = Queue()
    data = get_data()
    freeze = []

    for e, func in enumerate( functions , start=1):
        freeze.append( partial( wrapper_run, q, func, data, e ) )

    with ThreadPoolExecutor(max_workers=WORKER) as executor:
        for _ in executor.map(call, freeze):
            pass

    results = []
    while True:
        items = q.get()
        results.append( items )
        if q.empty():
            break
    save( results )


def main():
    _main()

def work():
    while True:
        try:
            main()
        except Exception as Er:
            log.error("Error {}".format(str(Er)), exc_info=True)
        finally:
            log.info("Sleep {}".format(TIMEOUT))
            time.sleep( TIMEOUT )


if __name__ == '__main__':
    # main()
    work()