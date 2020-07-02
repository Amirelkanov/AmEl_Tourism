#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Handling errors """

from flask import Blueprint, render_template

# Error Blueprint registration
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('Errors/500_error.html', title='Ой...')


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('Errors/404_error.html', title='Страница не найдена')


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('Errors/403_error.html', title='Недостаточно прав')


@errors.app_errorhandler(401)
def error_401(error):
    return render_template('Errors/401_error.html', title='Не авторизован')
