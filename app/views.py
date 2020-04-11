# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
import os
from flask import (
    jsonify,
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
import mistune
from flask.helpers import get_env
from flask.views import MethodView
from app import helpers

logger = helpers.get_logger(__name__)

def load_all_articles(dir_path: str) -> List[str]:
    all_files = os.listdir(dir_path)
    display_files = filter(lambda n: not n.startswith('.'), all_files)
    whole_paths = list(map(lambda n: os.path.join(dir_path, n), display_files))
    return whole_paths

def load_article_content(path: str) -> str:
    with open(path) as f:
        return f.read()

def render_content_to_markdown(content: str) -> str:
    markdown = mistune.Markdown()
    return markdown(content)

def article_list() -> List[Dict[str, str]]:
    if "site" not in g:
        return jsonify({'e': 'no site'})
    dir_path = g.site
    whole_paths = load_all_articles(dir_path)
    payload: List[Dict[str, str]] = []
    for path in whole_paths:
        payload.append(
            {
                'path': path,
                'title': (path.split('/')[-1]).split('.')[0],
                'description': 'desc',
                'last_modified': '昨天'
            }
        )
    return payload

def favicon_ico():
    return current_app.send_static_file("images/favicon.ico")

def index():
    payload = article_list()
    return render_template("index.html", payload=payload)

def article(title: str):
    a_list = article_list()
    ta = list(filter(lambda t: t['title'] == title, a_list))[0]
    content = load_article_content(ta['path'])
    paylaod = render_content_to_markdown(content)
    return render_template('detail.html', post={'title': title, 'content': paylaod})

def not_found(error: Exception) -> Tuple[str, int]:
    return render_template("404.html"), 404

def fetch_target_dir() -> Optional[str]:
    return os.getenv("TARGET_DIR")


def load_site_config():
    if "site" not in g:
        target = fetch_target_dir()
        if not target:
            return
        g.site = target

def about_me():
    return render_template("aboutme.html")

def init_app(app: Flask) -> None:
    app.add_url_rule("/articles", view_func=index, methods=["GET"])
    app.add_url_rule("/article/<string:title>", view_func=article, methods=["GET"])

    app.add_url_rule("/favicon.ico", view_func=favicon_ico)
    app.add_url_rule("/aboutme", view_func=about_me, methods=["GET"])

    app.register_error_handler(404, not_found)
    app.before_request(load_site_config)
