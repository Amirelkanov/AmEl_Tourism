#!/usr/bin/python
# -*- coding: utf-8 -*-

""" User Forms """

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    email = EmailField('Адрес эл. почты:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Создать аккаунт')


class LoginForm(FlaskForm):
    email = EmailField('Адрес эл. почты:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
