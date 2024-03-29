#!/usr/bin/python
# -*- coding: utf-8 -*-

""" User data related actions """

from flask import Blueprint, render_template, redirect
from flask_login import login_required, logout_user, login_user

from ..data.users import User
from ..extensions.const import min_length_of_password
from ..extensions.init_models import db, login_manager
from ..forms.user_forms import RegisterForm, LoginForm

# User Blueprint registration
user = Blueprint('user', __name__)


# Register form
@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        is_alert_hidden: bool = False

        # WARNING: This user already exists
        if User.query.filter(User.email == form.email.data).first():
            return render_template('Forms/register_form.html',
                                   title='Регистрация',
                                   alert_class='alert-warning',
                                   is_alert_hidden=is_alert_hidden,
                                   form=form,
                                   message="Такой пользователь уже есть")

        # ERROR: Passwords don't match
        if form.password.data != form.password_again.data:
            return render_template('Forms/register_form.html',
                                   title='Регистрация',
                                   form=form,
                                   alert_class='alert-danger',
                                   is_alert_hidden=is_alert_hidden,
                                   message="Пароли не совпадают")

        # WARNING: The length of the entered password is
        # less than the allowed length
        if len(form.password.data) < min_length_of_password:
            return render_template('Forms/register_form.html',
                                   title='Регистрация',
                                   form=form,
                                   alert_class='alert-warning',
                                   is_alert_hidden=is_alert_hidden,
                                   message=f"Минимальная длина пароля - "
                                           f"{min_length_of_password}")
        # -----------------------

        # Adding and committing changes to the DB
        new_user = User()
        new_user.name = form.name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)
        return redirect("/")

    return render_template('Forms/register_form.html', title='Регистрация',
                           form=form, alert_class='alert-danger',
                           is_alert_hidden=True)


# Login form
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user_by_email = User.query.filter(User.email == form.email.data).first()

        if user_by_email and user_by_email.check_password(form.password.data):
            login_user(user_by_email, remember=form.remember_me.data)
            return redirect("/")

        return render_template('Forms/login_form.html',
                               alert_class='alert-danger',
                               is_alert_hidden=False, form=form,
                               title='Авторизация',
                               message="Неправильный логин или пароль")

    return render_template('Forms/login_form.html', title='Авторизация',
                           form=form, alert_class='alert-danger',
                           is_alert_hidden=True)


@login_manager.user_loader
def load_user(user_id: int):
    """ Load user function
    :param user_id: user id in the database
    """
    return User.query.get(user_id)


# Logout function
@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
