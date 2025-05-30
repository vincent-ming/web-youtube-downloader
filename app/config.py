import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import services
from constants import TEMP_FILE_LIVE_TIME_MINUTES


def log_init():
    logs_folder = Path('./logs')
    if not logs_folder.exists():
        logs_folder.mkdir()

    log_level = 'INFO'
    log_path = './logs/wyd.log'
    log_format = '%(asctime)s | %(levelname)s | %(thread)d | %(filename)s-%(lineno)d | %(message)s'

    time_rotate_handler = TimedRotatingFileHandler(filename=log_path, when='midnight', interval=1,
                                                   backupCount=7)
    time_rotate_handler.suffix = '%Y-%m-%d'
    logging.basicConfig(level=log_level, format=log_format, handlers={time_rotate_handler})

    logging.getLogger('apscheduler').setLevel(logging.WARNING)


def scheduler_init():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(minute=f'*/{TEMP_FILE_LIVE_TIME_MINUTES}')
    scheduler.add_job(func=services.clean_tmp_folder, trigger=trigger)
    scheduler.start()
