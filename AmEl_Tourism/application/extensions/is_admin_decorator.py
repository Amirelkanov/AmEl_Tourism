#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Decorator that checks the user for administrator rights """

from functools import wraps

from flask_login import login_required, current_user
from flask_restful import abort

from ..data.users import User


def is_user_admin(function):
    @login_required
    @wraps(function)
    def wrapper(*args, **kwargs):

        if User.query.filter(User.id == current_user.id).first().is_admin:
            return function(*args, **kwargs)
        else:
            abort(403)

    return wrapper
