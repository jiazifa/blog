# -*- coding: utf-8 -*-

from flask import Blueprint, Flask

api = Blueprint("api", __name__)

def init_app(app: Flask) -> None:
    from . import views

    app.register_blueprint(api, url_prefix="/api")