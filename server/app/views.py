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

from .models import User, Category, Post, db
from .api.util import verify_auth, response_succ
from flask_login import current_user


def load_site_config():
    if "site" not in g:
        user = User.get_admin()
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


def manager_index():
    posts = Post.query.all()
    return render_template("/manager.html", posts=posts)


def edit():
    params = request.values or request.get_json()
    if not params or not params.get("pid"):
        return render_template("/edit.html")
    post = Post.query.get(params.get("pid"))
    return render_template("/edit.html", post=post)


def add_or_update_post():
    params = request.values or request.get_json()
    pid: int = params.get("pid") or None
    title: str = params.get("title")
    content: str = params.get("content")
    description: str = params.get("description")
    category_id: str = params.get("category_id")
    current_app.logger.info(params)
    if not pid:  # add
        post = Post(
            title=title,
            content=content,
            description=description,
            category_id=category_id,
        )
        db.session.add(post)
    else:
        post = Post.query.get(pid)
        post.title = title
        post.content = content
        post.description = description
        post.category_id = category_id
    db.session.commit()
    return response_succ({})

def delete(pid: int):
    p = Post.query.get(pid)
    db.session.delete(p)
    db.session.commit()
    return response_succ({"pid": pid})

class LoginMethodView(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        email = request.form.get("email", type=str)
        password = request.form.get("password", type=str)
        if not verify_auth(email, password):
            flash("账号或密码错误")
            return render_template("login.html")
        user: User = current_user
        if user.is_admin:
            return redirect(url_for("manager_index"))
        return redirect(url_for("index"))


class Dev(MethodView):
    def get(self, file: str):
        return render_template(file)


class IndexView(MethodView):
    def get(self):
        posts = [p.to_dict() for p in Post.query.all()]
        return render_template("index.html", posts=posts)

def post_detail(pid: int):
    post = Post.query.get(pid)
    return render_template("detail.html", post=post)

def init_app(app: Flask) -> None:
    app.add_url_rule("/index", view_func=IndexView.as_view("index"))
    if get_env() == "development":
        app.add_url_rule("/<string:file>", view_func=Dev.as_view("dev"))
    app.add_url_rule("/favicon.ico", view_func=favicon_ico)

    app.add_url_rule("/m_index", view_func=manager_index, methods=["GET"])
    app.add_url_rule("/edit", view_func=edit, methods=["GET"])
    app.add_url_rule("/delete/<int:pid>", view_func=delete)
    app.add_url_rule(
        "/addOrUpdate", view_func=add_or_update_post, methods=["POST"],
    )
    app.add_url_rule(
        "/login", view_func=LoginMethodView.as_view("login"), methods=["POST", "GET"]
    )
    app.add_url_rule("/detail/<int:pid>", view_func=post_detail, methods=["GET"])
    app.register_error_handler(404, not_found)
    app.before_request(load_site_config)
