import logging, sys, os

def get_logger(name):
    level = logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO'))
    formatter = logging.Formatter( '%(levelname)s [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)

    return log
    