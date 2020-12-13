import logging, os, hmac, hashlib

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
        ch = logging.FileHandler("/".join( [ os.getcwd(), path_file] ))

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


if __name__ == "__main__":
    secret = "t7T0YlFnYXk0Fx3JswQsDrViLg1Gh3DUU5Mr"
    params = {}
    params['api_key'] = "B2Rou0PLPpGqcU0Vu2"
    params['leverage'] = 100
    params['symbol'] = "BTCUSD"
    params['timestamp'] = "1542434791000"
    print(get_signature(secret, params))