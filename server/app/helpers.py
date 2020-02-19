# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional
import datetime
import time
import logging
import sys

from flask import current_app


def get_unix_time_tuple(
    date = datetime.datetime.now(),
    millisecond: bool = False
) -> str:
    """ get time tuple

    get unix time tuple, default `date` is current time

    Args:
        date: datetime, default is datetime.datetime.now()
        millisecond: if True, Use random three digits instead of milliseconds, default id False 

    Return:
        a str type value, return unix time of incoming time
    """
    time_tuple = time.mktime(date.timetuple())
    time_tuple = round(time_tuple * 1000) if millisecond else time_tuple
    second = str(int(time_tuple))
    return second


def get_date_from_time_tuple(unix_time: str = get_unix_time_tuple(), formatter: str = '%Y-%m-%d %H:%M:%S') -> str:
    """ translate unix time tuple to time

    get time from unix time

    Args:
        unix_time: unix time tuple
        formatter: str time formatter

    Return:
        a time type value, return time of incoming unix_time
    """
    if len(unix_time) == 13:
        unix_time = str(float(unix_time) / 1000)
    t = int(unix_time)
    time_locol = time.localtime(t)
    return time.strftime(formatter, time_locol)

loggers: Dict[str, logging.Logger] = {}

def get_logger(name: str) -> logging.Logger:
    """  获得一个logger 实例，用来打印日志
    Args: 
        name: logger的名称
    Return:
        返回一个logger实例
    """
    global loggers

    if not name:
        name = __name__

    has = loggers.get(name)
    if has:
        return has

    logger = logging.getLogger(name=name)
    logger.setLevel(current_app.config["LOG_LEVEL"])

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(current_app.config["LOG_LEVEL"])
    formatter = logging.Formatter(current_app.config["LOGGING_FORMATTER"])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    loggers[name] = logger

    return logger
