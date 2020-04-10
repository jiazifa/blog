# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from flask import (
    request,
    Flask,
    g,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    flash,
)
from flask.helpers import get_env
from flask.views import MethodView


def favicon_ico():
    return current_app.send_static_file("images/favicon.ico")


def not_found(error: Exception) -> Tuple[str, int]:
    return render_template("404.html"), 404


def about_me():
    return render_template("aboutme.html")

def init_app(app: Flask) -> None:
    
    app.add_url_rule("/favicon.ico", view_func=favicon_ico)
    app.add_url_rule("/aboutme", view_func=about_me, methods=["GET"])

    app.register_error_handler(404, not_found)
