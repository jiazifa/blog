# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from flask import request, Blueprint
from flask.views import MethodView

import app

api = Blueprint("blog", __name__)
app.fetch_blueprint(api, "/")

class IndexView(MethodView):
    def get(self):
        return "HI"

api.add_url_rule('/index', view_func=IndexView.as_view('index'))