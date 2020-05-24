#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, abort

from ...data.articles import Category
from ...extensions.init_models import db
from ...extensions.is_admin_decorator import is_user_admin
from ...forms.admin_forms import CategoryForm

category_actions = Blueprint('category_actions', __name__)


# Page showing categories
@category_actions.route('/categories')
@category_actions.route('/categories/sort_by/<string:sort_by_element>/is_reversed=<int:is_reversed>')
@is_user_admin
def categories(sort_by_element='id', is_reversed=0):
    sorting_elem = Category.__dict__[sort_by_element]
    order_by_arg = db.desc(sorting_elem) if is_reversed else sorting_elem
    return render_template('Admin/categories.html', title='Категории',
                           columns_name=Category.category_columns_name, sort_by_element=sort_by_element,
                           is_reversed=(is_reversed, int(not is_reversed)),
                           list_of_categories=Category.query.order_by(order_by_arg).all())


# Add category form
@category_actions.route('/add_category', methods=['GET', 'POST'])
@is_user_admin
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        category.name_of_category = form.name_of_category.data
        db.session.add(category)
        db.session.commit()
        return redirect('/categories')

    return render_template('Forms/category_form.html', title='Добавление категории',
                           form=form, submit_button_text="Добавить")


# Edit category form
@category_actions.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@is_user_admin
def edit_category(category_id):
    form = CategoryForm()
    if request.method == 'GET':
        category = Category.query.filter_by(id=category_id).first()
        if category:
            form.name_of_category.data = category.name_of_category
        else:
            abort(404)

    if form.validate_on_submit():

        category = Category.query.filter_by(id=category_id).first()
        if category:
            category.name_of_category = form.name_of_category.data
            db.session.add(category)
            db.session.commit()
        return redirect('/categories')

    return render_template('Forms/category_form.html', title='Редактирование категории',
                           form=form, submit_button_text="Сохранить")


# Delete category
@category_actions.route('/delete_category/<int:category_id>', methods=['GET', 'POST'])
@is_user_admin
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    else:
        abort(404)
    return redirect('/categories')
