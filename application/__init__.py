#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Application initialization """

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from .config import Config
from .extensions.init_models import db, login_manager
from .routes import errors_handler, user_data, static_pages
from .routes.actions import account_actions, article_actions, category_actions, user_actions


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate()

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # ----- Blueprint registration -----
    app.register_blueprint(static_pages.main)
    app.register_blueprint(user_data.user)

    app.register_blueprint(article_actions.article_actions)
    app.register_blueprint(user_actions.user_actions)
    app.register_blueprint(category_actions.category_actions)
    app.register_blueprint(account_actions.account_actions)

    app.register_blueprint(errors_handler.errors)
    # -----------------------------

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return app
