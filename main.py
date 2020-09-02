import configparser
import requests, time
from multiprocessing import Process, SimpleQueue
from threading import Thread
from queue import Queue
from tools import log as lo
from custom import functions



config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
URL  = args['url']
PATH = args['result_path']
NAME = args['name']
TIMEOUT = float( args['timeout'] )

log = lo(NAME, "main.log")

def comma(float):
    res = "{}".format( float )
    res = res.replace(".",",")
    return res

def get_data():
    response = requests.get( URL )
    if response.status_code == 200:
        return response.json()
    raise ValueError

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


def _main():
    q = Queue()
    data = get_data()
    processes = []

    for e, func in enumerate( functions , start=1):
        processes.append( Thread(target=wrapper_run, args =  (q, func, data, e ) ) )

    [x.start() for x in processes]
    [x.join() for x in processes]
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