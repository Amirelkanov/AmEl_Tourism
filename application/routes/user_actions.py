#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, abort

from ..data.users import User
from ..extensions.init_models import db
from ..extensions.is_admin_decorator import is_user_admin

user_actions = Blueprint('_user_', __name__)


# Users table
@user_actions.route('/users', endpoint='users')
@user_actions.route('/users/sort_by/<string:sort_by_element>/is_reversed=<int:is_reversed>', endpoint='users')
@is_user_admin
def users(sort_by_element='id', is_reversed=0):
    sorting_elem = User.__dict__[sort_by_element]
    order_by_arg = db.desc(sorting_elem) if is_reversed else sorting_elem
    return render_template('Admin/users.html', title='Список пользователей',
                           columns_name=User.user_columns_name, sort_by_element=sort_by_element,
                           is_reversed=(is_reversed, int(not is_reversed)),
                           list_of_users=User.query.order_by(order_by_arg).all())


# Setting user role (admin / not admin)
@user_actions.route('/admin_setting/<string:action>/<int:user_id>')
@is_user_admin
def admin_setting(action, user_id):
    user = User.query.filter(User.id == user_id).first()
    if user and action in ['add', 'remove']:
        user.is_admin = True if action == 'add' else False
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    abort(404)
