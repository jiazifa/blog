# -*- coding: utf-8 -*-

from typing import List, Any, Tuple
from os import path, listdir

from flask import Flask, Blueprint

__root_dir = path.dirname(path.abspath(__name__))

blueprints: List[Tuple[Blueprint, str]] = []

def fetch_blueprint(blueprint: Blueprint, prefix: str):
    global blueprints
    t: Tuple[Blueprint, str] = (blueprint, prefix)
    blueprints.append(t)

def _regist_blueprint(app: Flask, src_dir: str):
    app_dir = path.join(__root_dir, src_dir)
    for routes in listdir(app_dir):
        route_path: str = path.join(app_dir, routes)
        if (not path.isfile(route_path)) \
                and routes != 'static' \
                and routes != 'templates' \
                and not routes.startswith('__'):
            __import__('app.' + routes)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint[0], url_prefix=blueprint[1])

def create_app(env: str) -> Flask:
    app = Flask(__name__)
    _regist_blueprint(app, 'app')
    return app