#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..extensions.init_models import db


class TGUserInfo(db.Model):
    """ TG User info model initialization class """

    __tablename__ = 'tg_user_info'
    id = db.Column(db.Integer, primary_key=True)
    coords = db.Column(db.String, nullable=True)
    page = db.Column(db.Integer, nullable=False, default=1)
