# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from flask import request, Flask, g, current_app, render_template, send_from_directory
from flask.views import MethodView

def load_site_config():
    if "site" not in g:
        g.site = {
            "title": "博客",
            "name": "treee_",
            "icp": "CF5504933",
            "url": "http://sfaf",
            "owner": "treee",
        }

def favicon_ico():
    return current_app.send_static_file("images/favicon.ico")

def not_found(error: Exception) -> Tuple[str, int]:
    return render_template("404.html"), 404

class Dev(MethodView):
    def get(self, file: str):
        return render_template(file)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html', name='sadfas')

def init_app(app: Flask) -> None:
    app.add_url_rule('/index', view_func=IndexView.as_view('home'))
    app.add_url_rule('/<string:file>', view_func=Dev.as_view('dev'))
    app.add_url_rule('/favicon.ico', view_func=favicon_ico)

    app.register_error_handler(404, not_found)
    app.before_request(load_site_config)