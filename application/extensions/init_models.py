#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Initialization of flask models """

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
