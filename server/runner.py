# -*- coding: utf-8 -*-
import os

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app.app import create_app

env: str = os.environ.get('FLASK_ENV') or 'default'
main_app = create_app(env)

application = main_app

if __name__ == "__main__":
    application.run(host='localhost', port=9000, debug=True)