# -*- coding: utf-8 -*-

from typing import List, Any, Tuple, Optional
from os import path, listdir

from flask import Flask, Blueprint
from flask.helpers import get_env

from . import views, config, models

__root_dir = path.dirname(path.abspath(__name__))

def create_app(env: Optional[str] = None) -> Flask:
    env = env or get_env()
    app = Flask(__name__)
    app.config.from_object(config.config_dict[env])
    views.init_app(app)
    models.init_app(app)
    app.config["SECRET_KEY"] = "123456"
    return app