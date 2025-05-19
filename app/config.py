import logging
import os
from logging.handlers import TimedRotatingFileHandler


def log_init():
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    log_level = 'INFO'
    log_path = './logs/wyd.log'
    log_format = '%(asctime)s | %(levelname)s | %(thread)d | %(filename)s-%(lineno)d | %(message)s'

    time_rotate_handler = TimedRotatingFileHandler(filename=log_path, when='midnight', interval=1,
                                                   backupCount=7)
    time_rotate_handler.suffix = '%Y-%m-%d'
    logging.basicConfig(level=log_level, format=log_format, handlers={time_rotate_handler})
