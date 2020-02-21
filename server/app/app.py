# -*- coding: utf-8 -*-

from typing import List, Any, Tuple, Optional
from os import path, listdir

from flask import Flask, Blueprint
from flask.helpers import get_env

from flask_login import LoginManager
from . import views, config, models

__root_dir = path.dirname(path.abspath(__name__))

def create_app(env: Optional[str] = None) -> Flask:
    env = env or get_env()
    app = Flask(__name__)
    app.config.from_object(config.config_dict[env])
    views.init_app(app)
    models.init_app(app)
    
    login_manager = LoginManager(app)
    
    @login_manager.user_loader
    def get_user(uid: int):
        return models.User.query.get(uid)
    return app