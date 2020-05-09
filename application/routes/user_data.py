#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect
from flask_login import login_required, logout_user, login_user

from ..data.users import User
from ..extensions.init_models import db
from ..extensions.init_models import login_manager
from ..forms.user_forms import RegisterForm, LoginForm

user = Blueprint('user', __name__)


# Register form
@user.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('Forms/register_form.html', title='Регистрация',
                                   form=form,
                                   alert="alert alert-danger",
                                   message="Пароли не совпадают")

        if User.query.filter(User.email == form.login_or_email.data).first():
            return render_template('Forms/register_form.html', title='Регистрация',
                                   alert="alert alert-danger",
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()
        user.name = form.name.data
        user.email = form.login_or_email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template('Forms/register_form.html', title='Регистрация', form=form)


# Login form
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('Forms/login_form.html',
                               alert="alert alert-danger",
                               form=form,
                               message="Неправильный логин или пароль")
    return render_template('Forms/login_form.html', title='Авторизация', form=form)


# Load user function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Logout function
@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
