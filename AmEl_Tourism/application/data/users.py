#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Initializing columns for table User """

import datetime

from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions.init_models import db


class User(db.Model, UserMixin, SerializerMixin):
    """ User model initialization class """

    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String,
                     nullable=False)
    email = db.Column(db.String,
                      unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    registration_date = db.Column(db.DateTime,
                                  default=datetime.datetime.now)

    user_columns_name = {
        'id': 'ID',
        'name': 'Имя пользователя',
        'email': 'Электронная почта',
        'registration_date': 'Дата регистрации',
        'is_admin': 'Админ'
    }

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class UserInfo(db.Model):
    """ User info model initialization class """

    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    coords = db.Column(db.String, nullable=True)
    page = db.Column(db.Integer, nullable=False, default=1)
