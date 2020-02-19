# -*- coding: utf-8 -*-

from typing import Union, Dict, Any

from flask import abort, g, json, jsonify, request
from flask.views import MethodView
from flask_login import current_user

from ..models import Category, Comment, Post, Tag, db, generate_password_hash, User
from . import api
from .util import verify_auth, response_error, response_succ

TOKEN_HEADER = "X-Token"

# @api.before_app_request
# def authenticate_view():
#     if request.path == "/api/user/login":
#         return
#     token = request.headers.get(TOKEN_HEADER)
#     if not token or not verify_auth(token):
#         return response_error(50001, "error Token")

def login():
    data = request.get_json()
    if not verify_auth(data.get("username"), data.get("password")):
        return response_error(2, msg="账号或密码错误")
    return response_succ({"token": current_user.generate_token().decode()})

api.add_url_rule("/user/login", view_func=login, methods=["POST"])