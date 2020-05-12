#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Application initialization """

from flask import Flask

from commands import create_tables
from .extensions.init_models import db, login_manager
from .routes import errors_handler, article_actions, user_data, category_actions, static_pages, user_actions


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Init secret key
    app.config['SECRET_KEY'] = 'AmEl-Tourism-key'

    # Init recaptcha
    app.config["RECAPTCHA_PUBLIC_KEY"] = "6Leg2OkUAAAAANYckFuHF37iwk-qv2X0QTLK2ANu"
    app.config["RECAPTCHA_PRIVATE_KEY"] = "6Leg2OkUAAAAAJkKR0CIhMxxIS5eu65_dZYZW4oF"

    # Init database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wgfebwadpolfvi:61a91a8bd3230cc9ab9a020ba3517faeb998eedbe87723' \
                                            '7c112d29114ff8736f@ec2-52-71-55-81.compute-1.amazonaws.com:5432' \
                                            '/d2j2hkmdp0uifl'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(static_pages.main)
    app.register_blueprint(user_data.user)

    app.register_blueprint(article_actions.article_actions)
    app.register_blueprint(user_actions.user_actions)
    app.register_blueprint(category_actions.category_actions)

    app.register_blueprint(errors_handler.errors)

    app.cli.add_command(create_tables)

    return app
