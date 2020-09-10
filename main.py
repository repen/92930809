import configparser, time
from requests.auth import AuthBase
from threading import Thread
from queue import Queue
from tools import log as lo
from custom import functions
from tools import generate_signature
import requests
config = configparser.ConfigParser()
config.read('setting.conf')

args = config['site']
URL  = args['url']
PATH = args['result_path']
NAME = args['name']
TIMEOUT = float( args['timeout'] )

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
    try:
        apiKey    = "hc_q3pDXXV4N3iIWQw6US27o"
        apiKey    = "Lj1Ows71OdYO9P4W6OjdPpk7"
        apiSecret = "hT-vagXM1xNMB4jrxRH75svQMAlegMsxX36lNcaV3JJl82Vk"
        apiSecret = "ETC4AYMoDHpoS44JgSN2WOfe1-5Ym4TKcRTCmKyPb2EZsRAl"

        response  = requests.get( URL, auth=APIKeyAuthWithExpires(apiKey, apiSecret), timeout=2.001)

        log.info( "Response {} limit: {}".format( response, response.headers["X-RateLimit-Remaining"] ) )
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

def test():
    z = 0
    while True:
        data = get_data()
        functions[-1](data)
        z += 1
        time.sleep(0.1)

if __name__ == '__main__':
    # test()
    # main()
    work()