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
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask.helpers import get_env
from flask.views import MethodView
from app import helpers

logger = helpers.get_logger(__name__)

def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )

class HighlightMixin(object):
    def block_code(self, text, lang):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles')
        return block_code(text, lang, inlinestyles, False)


class TocRenderer(HighlightMixin, mistune.Renderer):
    pass

def load_all_articles(dir_path: str) -> List[str]:
    all_files = os.listdir(dir_path)
    display_files = filter(lambda n: not n.startswith('.'), all_files)
    whole_paths = list(map(lambda n: os.path.join(dir_path, n), display_files))
    return whole_paths

def load_article_content(path: str) -> str:
    with open(path) as f:
        return f.read()

def render_content_to_markdown(content: str) -> str:
    renderer = TocRenderer(linenos=True, inlinestyles=False)
    markdown = mistune.Markdown(escape=True, renderer=renderer)
    return markdown(content)

def article_list() -> List[Dict[str, str]]:
    if "site" not in g:
        return jsonify({'e': 'no site'})
    dir_path = g.site['target_dir']
    whole_paths = load_all_articles(dir_path)
    payload: List[Dict[str, str]] = []
    for path in whole_paths:
        filename = path.split('/')[-1].split('.')[0]
        title = filename.split('-')[-1]
        publish_date = "-".join(filename.split('-')[:-1])
        payload.append(
            {
                'path': path,
                'filename': filename,
                'title': title,
                'description': publish_date,
                'last_modified': '昨天'
            }
        )
    return payload

def favicon_ico():
    return current_app.send_static_file("images/favicon.ico")

def index():
    payload = article_list()
    return render_template("index.html", title='tree', payload=payload)

def article(title: str):
    a_list = article_list()
    ta = list(filter(lambda t: t['title'] == title, a_list))[0]
    content = load_article_content(ta['path'])
    paylaod = render_content_to_markdown(content)
    return render_template('detail.html', title=title, post={'title': title, 'content': paylaod})

def not_found(error: Exception) -> Tuple[str, int]:
    return render_template("404.html"), 404

def fetch_target_dir() -> Optional[str]:
    return os.getenv("TARGET_DIR")


def load_site_config():
    if "site" not in g:
        target = fetch_target_dir()
        if not target:
            return
        g.site = {
            'target_dir': target,
            'title': 'Tree',
        }

def about_me():
    return render_template("aboutme.html")

def init_app(app: Flask) -> None:
    app.add_url_rule("/", view_func=index, methods=["GET"])
    app.add_url_rule("/article/<string:title>", view_func=article, methods=["GET"])

    app.add_url_rule("/favicon.ico", view_func=favicon_ico)
    app.add_url_rule("/aboutme", view_func=about_me, methods=["GET"])

    app.register_error_handler(404, not_found)
    app.before_request(load_site_config)
