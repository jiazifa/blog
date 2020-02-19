# -*- coding: utf-8 -*-

from typing import Union, Dict, Any, Optional, List, Tuple
from flask import jsonify
from flask_login import current_user, login_user
from ..models import User


def verify_auth(username_or_token: str, password: Union[None, str]) -> bool:
    if password:
        user: Union[None, User] = User.query.filter_by(
            username=username_or_token, is_admin=True
        ).first()
        if not user or not user.check_password(password):
            return False
    else:
        user = User.verify_auto_token(username_or_token)
        if not user or not user.is_admin:
            return False
    if not current_user or current_user.get_id() != user.get_id():
        login_user(user)
    return True


def response_succ(
    body: Union[Dict[str, Any], List[Any]], toast: Union[str, None]
) -> str:
    result = {"data": body, "msg": toast, "code": 20000}
    return jsonify(result)


def response_error(
    error_code: int, msg: str, body: Union[Dict[str, Any], List[Any]] = {}
) -> str:

    if msg is None:
        raise ValueError("error Msg can't be None")
    data = {"code": error_code, "message": msg, "data": body}
    return jsonify(data) or jsonify({"error": "cant jsonify"})
