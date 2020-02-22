# -*- coding: utf-8 -*-

import os
from os import path

_here = path.dirname(__name__)

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "flask blog")
    """SQLALCHEMY配置"""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + path.join(_here, "db.sqlite3")
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


    DEFAULT_ADMIN_PASSWORD = "admin"
    BLOG_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    ADMIN_EMAIL = "2332532718@qq.com"
    
    # logging
    LOG_LEVEL = "DEBUG"  # 日志输出等级
    LOGGING_FORMATTER = "%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s"  # 每条日志输出格式


class ProductionConfig(BaseConfig):

    if "DATABASE_URL" in os.environ:  # Heroku environment
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(_here, "db.sqlite3")

    SERVER_NAME = "blog"


class DevelopConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    TESTING = True

config_dict = {
    "production": ProductionConfig,
    "development": DevelopConfig,
    "testing": TestingConfig,
    "default": DevelopConfig,
}