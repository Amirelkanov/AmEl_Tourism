#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Application initialization """

from flask import Flask

from .commands import create_tables
from .extensions.init_models import db, login_manager
from .routes import errors_handler, user_data, static_pages
from .routes.actions import account_actions, article_actions, category_actions, user_actions


def create_app(config_file='settings.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)

    # ----- Blueprint registration -----
    app.register_blueprint(static_pages.main)
    app.register_blueprint(user_data.user)

    app.register_blueprint(article_actions.article_actions)
    app.register_blueprint(user_actions.user_actions)
    app.register_blueprint(category_actions.category_actions)
    app.register_blueprint(account_actions.account_actions)

    app.register_blueprint(errors_handler.errors)
    # -----------------------------

    app.cli.add_command(create_tables)

    return app
