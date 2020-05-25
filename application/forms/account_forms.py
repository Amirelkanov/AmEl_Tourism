#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Account Forms """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EmailForm(FlaskForm):
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Сохранить')


class PasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль:', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль:', validators=[DataRequired(), Length(min=8)])
    new_password_again = PasswordField('Повторите новый пароль:', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Сохранить')
