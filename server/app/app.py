# -*- coding: utf-8 -*-

from typing import List, Any, Tuple, Optional
from os import path, listdir

from flask import Flask, Blueprint

from . import views

__root_dir = path.dirname(path.abspath(__name__))

def create_app(env: Optional[str]) -> Flask:
    app = Flask(__name__)
    views.init_app(app)
    return app