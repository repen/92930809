import logging, os

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
    formatter = logging.Formatter('%(asctime)s : line %(lineno)d : %(name)s : %(levelname)s : %(message)s')
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