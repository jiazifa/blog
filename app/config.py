# -*- coding: utf-8 -*-

import os
from os import path

_here = path.dirname(__name__)

class BaseConfig:
    
    # logging
    LOG_LEVEL = "DEBUG"  # 日志输出等级
    LOGGING_FORMATTER = "%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s"  # 每条日志输出格式


class ProductionConfig(BaseConfig):

    SERVER_NAME = "blog"


class DevelopConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass
    TESTING = True

config_dict = {
    "production": ProductionConfig,
    "development": DevelopConfig,
    "testing": TestingConfig,
    "default": DevelopConfig,
}