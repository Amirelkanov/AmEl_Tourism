#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from .config import Config
from .extensions.init_models import db, login_manager
from .routes import errors_handler, user_data, static_pages
from .routes.actions import account_actions
from .routes.actions.admin import article_actions, category_actions, \
    user_actions


# Create app function
def create_app():

    # Init app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init db migrate
    migrate = Migrate()

    # Init models
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

    # Adding "db" command
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return app
