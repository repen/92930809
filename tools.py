import logging, os, hmac, hashlib, re
from itertools import zip_longest
from urllib.parse import urlparse


def log(*args, **kwargs):
    name_logger = args[0]
    path_file   = args[1]
    write = kwargs.setdefault("write", False)
    # создаём logger
    logger = logging.getLogger(name_logger)
    logger.setLevel( logging.DEBUG )

    # создаём консольный handler и задаём уровень
    if not write:
        ch = logging.StreamHandler()
    else:
        # log write in disk
        ch = logging.FileHandler(os.path.join( os.getcwd(), path_file) )

    ch.setLevel(logging.DEBUG)

    # создаём formatter
    formatter = logging.Formatter('%(asctime)s : line %(lineno)-3s : %(name)s : %(levelname)s : %(message)s')
    # %(lineno)d :
    # добавляем formatter в ch
    ch.setFormatter(formatter)

    # добавляем ch к logger
    logger.addHandler(ch)
    # Api
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    return logger


def generate_signature(secret, verb, url, nonce, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')

    # print "Computing HMAC: %s" % verb + path + str(nonce) + data
    message = verb + path + str(nonce) + data

    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    return signature



class Info:
    def __init__(self, *args):
        self.path = args[0]
        with open(self.path) as f:
            self.data = f.read()


        self.plus    = re.findall(r"\+", self.data)
        self.numbers = re.findall(r"\d\.\d+", self.data)

    def clear_plus(self):
        self.plus = []

    def length_plus(self):
        return len(self.plus)

    def add_plus(self):
        self.plus.append("+")

    def __str__(self):
        res = list( zip_longest(self.numbers, self.plus, fillvalue=' ') )
        res = [" ".join(x) for x in res]
        res = "\n".join(res)
        return res

    def save(self):
        with open(self.path, "w") as f:
            f.write(self.__str__())

    def get_num(self):
        index = len( self.plus )
        return float( self.numbers[ index ] )



