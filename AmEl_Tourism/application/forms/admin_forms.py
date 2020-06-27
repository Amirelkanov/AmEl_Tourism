#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Admin Forms """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Заголовок:', validators=[DataRequired()])
    coords_of_place = StringField('Координаты места:',
                                  validators=[DataRequired()])
    text = TextAreaField('Введите текст для статьи:',
                         validators=[DataRequired()])
    category = SelectField('Выберите категорию:',
                           validators=[DataRequired()])
    submit = SubmitField()


class CategoryForm(FlaskForm):
    name_of_category = StringField('Название категории:',
                                   validators=[DataRequired()])
    submit = SubmitField()
