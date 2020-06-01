#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from ...data.users import User
from ...extensions.const import min_length_of_password
from ...extensions.formatted_datetime import get_formatted_datetime
from ...extensions.init_models import db
from ...forms.account_forms import NameForm, EmailForm, PasswordForm

account_actions = Blueprint('account_actions', __name__)


# Page showing account info
@account_actions.route('/account')
@login_required
def account():
    return render_template('account.html', title='Аккаунт',
                           user_registration_date=get_formatted_datetime(current_user.registration_date))


# Edit name form
@account_actions.route('/account/name', methods=['GET', 'POST'])
@login_required
def edit_name():
    form = NameForm()
    if request.method == 'GET':
        form.name.data = current_user.name

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        is_alert_hidden = False

        if not user.check_password(form.password.data):
            return render_template('Forms/name_form.html', title='Изменение имени',
                                   is_alert_hidden=is_alert_hidden, form=form,
                                   message='Введён неправильный пароль', alert_class='alert-danger')

        if user:
            user.name = form.name.data
            db.session.add(user)
            db.session.commit()

        return render_template('Forms/name_form.html', title='Изменение имени',
                               is_alert_hidden=is_alert_hidden, form=form,
                               message='Имя успешно изменено!', alert_class='alert-success')

    return render_template('Forms/name_form.html', title='Изменение имени',
                           form=form, is_alert_hidden=True)


# Edit email form
@account_actions.route('/account/email', methods=['GET', 'POST'])
@login_required
def edit_email():
    form = EmailForm()
    if request.method == 'GET':
        form.email.data = current_user.email

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        is_alert_hidden = False

        if not user.check_password(form.password.data):
            return render_template('Forms/email_form.html', title='Изменение почты',
                                   is_alert_hidden=is_alert_hidden, form=form,
                                   message='Введён неправильный пароль', alert_class='alert-danger')

        if user:
            if User.query.filter_by(email=form.email.data).first().id != current_user.id:
                form.email.data = current_user.email
                return render_template('Forms/email_form.html', title='Изменение почты',
                                       is_alert_hidden=is_alert_hidden, form=form,
                                       message='Введёный адрес электронной почты уже используется на другом аккаунте',
                                       alert_class='alert-warning')
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()

        return render_template('Forms/email_form.html', title='Изменение почты',
                               is_alert_hidden=is_alert_hidden, form=form,
                               message='Адрес почты успешно изменён!', alert_class='alert-success')

    return render_template('Forms/email_form.html', title='Изменение почты', form=form, is_alert_hidden=True)


# Edit password form
@account_actions.route('/account/password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = PasswordForm()
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        is_alert_hidden = False

        if not user.check_password(form.current_password.data):
            return render_template('Forms/password_form.html', title='Изменение пароля',
                                   is_alert_hidden=is_alert_hidden, form=form,
                                   message='Текущий пароль введён неправильно',
                                   alert_class='alert-danger')

        if user:
            if form.new_password.data != form.new_password_again.data:
                return render_template('Forms/password_form.html', title='Изменение пароля',
                                       is_alert_hidden=is_alert_hidden, form=form,
                                       message='Новые пароли не совпадают',
                                       alert_class='alert-warning')

            if len(form.new_password.data) < min_length_of_password:
                return render_template('Forms/password_form.html', title='Изменение пароля',
                                       form=form,
                                       alert_class='alert-warning', is_alert_hidden=is_alert_hidden,
                                       message=f"Минимальная длина пароля - {min_length_of_password}")

            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()

        return render_template('Forms/password_form.html', title='Изменение пароля',
                               is_alert_hidden=is_alert_hidden, form=form,
                               message='Пароль успешно изменён!', alert_class='alert-success')

    return render_template('Forms/password_form.html', title='Изменение пароля',
                           form=form, is_alert_hidden=True)
