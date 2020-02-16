# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from flask import request, Flask, Blueprint, render_template
from flask.views import MethodView

class Dev(MethodView):
    def get(self, file: str):
        return render_template(file)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html', name='sadfas')

def init_app(app: Flask) -> None:
    app.add_url_rule('/index', view_func=IndexView.as_view('index'))
    app.add_url_rule('/<string:file>', view_func=Dev.as_view('dev'))