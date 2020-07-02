#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Category related actions """

from flask import Blueprint, render_template, redirect, request, abort

from ....data.articles import Category
from ....extensions.init_models import db
from ....extensions.is_admin_decorator import is_user_admin
from ....forms.admin_forms import CategoryForm

# Category actions Blueprint registration
category_actions = Blueprint('category_actions', __name__)


@category_actions.route('/categories')
@category_actions.route('/categories/sort_by/<string:sort_by_element>/'
                        'is_reversed=<int:is_reversed>')
@is_user_admin
def categories(sort_by_element: str = 'id', is_reversed: int = 0):
    """ Showing page with list of categories
    :param sort_by_element: element to sort the user table by
    :param is_reversed: whether sorting is reversed
    """

    sorting_elem: str = Category.__dict__.get(sort_by_element, 'id')
    order_by_arg = db.desc(sorting_elem) if is_reversed else sorting_elem
    return render_template('Admin/categories.html', title='Список категорий',
                           columns_name=Category.category_columns_name,
                           sort_by_element=sort_by_element,
                           is_reversed=(is_reversed, int(not is_reversed)),
                           list_of_categories=Category.query.order_by(
                               order_by_arg).all())


# Add category form
@category_actions.route('/add_category', methods=['GET', 'POST'])
@is_user_admin
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # Adding and committing changes to the DB
        category = Category()
        category.name_of_category = form.name_of_category.data
        db.session.add(category)
        db.session.commit()

        return redirect('/categories')

    return render_template('Forms/category_form.html',
                           title='Добавление категории',
                           form=form, submit_button_text="Добавить")


@category_actions.route('/edit_category/<int:category_id>',
                        methods=['GET', 'POST'])
@is_user_admin
def edit_category(category_id: int):
    """ Edit category form
    :param category_id: category (or rather, its id) to edit
    """

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
            # Adding and committing changes to the DB
            category.name_of_category = form.name_of_category.data
            db.session.add(category)
            db.session.commit()
        return redirect('/categories')

    return render_template('Forms/category_form.html',
                           title='Редактирование категории',
                           form=form, submit_button_text="Сохранить")


@category_actions.route('/delete_category/<int:category_id>',
                        methods=['GET', 'POST'])
@is_user_admin
def delete_category(category_id: int):
    """ Deleting category
    :param category_id: category (or rather, its id) to delete
    """

    category = Category.query.filter_by(id=category_id).first()
    if category:
        # Removing a category from the DB
        db.session.delete(category)
        db.session.commit()
    else:
        abort(404)
    return redirect('/categories')
