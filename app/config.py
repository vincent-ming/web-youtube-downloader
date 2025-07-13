import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import services
from constants import TEMP_FILE_LIVE_TIME_MINUTES


def log_init():
    logs_folder = Path('./logs')
    logs_folder.mkdir(exist_ok=True)

    log_level = logging.INFO
    log_path = logs_folder / 'wyd.log'
    log_format = '%(asctime)s | %(levelname)s | %(thread)d | %(filename)s-%(lineno)d | %(message)s'
    formatter = logging.Formatter(log_format)

    file_handler = TimedRotatingFileHandler(filename=log_path, when='midnight', interval=1,
                                            backupCount=7)
    file_handler.setFormatter(formatter)
    file_handler.suffix = '%Y-%m-%d'

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logging.basicConfig(level=log_level, handlers={file_handler, stream_handler})

    logging.getLogger('apscheduler').setLevel(logging.WARNING)


def scheduler_init():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(minute=f'*/{TEMP_FILE_LIVE_TIME_MINUTES}')
    scheduler.add_job(func=services.clean_tmp_folder, trigger=trigger)
    scheduler.start()
