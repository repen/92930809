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
        ch = logging.FileHandler( os.path.join( os.getcwd(), path_file ) )

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


def get_signature(secret: str, req_params: dict):
    """
    :param secret    : str, your api-secret
    :param req_params: dict, your request params
    :return: signature
    """
    _val = '&'.join([str(k)+"="+str(v) for k, v in sorted(req_params.items()) if (k != 'sign') and (v is not None)])
    # print(_val)
    return str(hmac.new(bytes(secret, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())


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



