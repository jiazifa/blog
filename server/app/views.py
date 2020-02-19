# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from flask import request, Flask, g, current_app, render_template, send_from_directory, redirect, url_for, flash
from flask.helpers import get_env
from flask.views import MethodView

from .models import User, Category, db
from .api.util import verify_auth

def load_site_config():
    if "site" not in g:
        # user = User.get_admin()
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


class LoginMethodView(MethodView):
    def get(self):
        c = Category(text="test content")
        db.session.add(c)
        db.session.commit()
        return render_template('login.html')

    def post(self):
        email = request.form.get("email", type=str)
        password = request.form.get("password", type=str)
        if not verify_auth(email, password):
            flash("账号或密码错误")
            return render_template("login.html")
        return redirect(url_for('/index'))
    
class Dev(MethodView):
    def get(self, file: str):
        return render_template(file)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html', name='sadfas')

def init_app(app: Flask) -> None:
    app.add_url_rule('/index', view_func=IndexView.as_view('/index'))
    if get_env() == "development":
        app.add_url_rule('/<string:file>', view_func=Dev.as_view('dev'))
    app.add_url_rule('/favicon.ico', view_func=favicon_ico)

    app.add_url_rule('/login', view_func=LoginMethodView.as_view('login'), methods=["POST", "GET"])

    app.register_error_handler(404, not_found)
    app.before_request(load_site_config)