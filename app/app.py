# -*- coding: utf-8 -*-

from typing import List, Any, Tuple, Optional
import os

from flask import Flask, Blueprint
from flask.helpers import get_env

from . import views, config

__root_dir = os.path.dirname(os.path.abspath(__name__))

def create_app(env: Optional[str] = None) -> Flask:
    env = env or get_env()
    print(os.getcwd())
    app = Flask(__name__)
    app.config.from_object(config.config_dict[env])
    views.init_app(app)    
    return app
