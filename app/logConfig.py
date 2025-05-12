import logging

def init():
    log_level = 'INFO'
    log_path = './logs/wyd.log'
    log_format = '%(asctime)s | %(levelname)s | %(thread)d | %(filename)s-%(lineno)d | %(message)s'
    logging.basicConfig(filename=log_path, level=log_level, format=log_format)