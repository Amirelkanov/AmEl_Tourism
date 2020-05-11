#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, abort
from flask_login import current_user
from werkzeug.utils import secure_filename

from ..data.articles import Category, Article
from ..extensions.const import min_length_of_text
from ..extensions.img_dirs import TITLE_IMG_DIR, ARTICLE_IMG_DIR
from ..extensions.img_tags import img_tag, group_img_tag
from ..extensions.init_models import db
from ..extensions.is_admin_decorator import is_user_admin
from ..extensions.load_images import load_images
from ..forms.admin_forms import ArticleForm

article_actions = Blueprint('article_actions', __name__)


# Article add form
@article_actions.route('/add_article', methods=['GET', 'POST'])
@is_user_admin
def add_article():
    title_image_name, article_images = 'Титульное изображение', 'Загрузить изображения'
    form = ArticleForm()

    form.category.choices = [(i.id, i.name_of_category) for i in Category.query.all()]

    if request.method == 'POST':
        article_text = form.text.data.replace('\r\r', '<br>')
        if len(article_text.split()) < min_length_of_text:
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert="alert alert-danger",
                                   message="Текст статьи слишком маленький", title_image_name=title_image_name,
                                   article_images=article_images, min_length_of_text=min_length_of_text,
                                   submit_button_text='Опубликовать')

        # ----------------------- Formatting text for article card -----------------------

        # Downloading title images
        list_of_title_imgs = request.files.getlist('thumbnail-img')
        title_filename = load_images(list_of_title_imgs)[0]

        # Downloading article images
        article_images = request.files.getlist('article-images')
        name_of_article_images = \
            [secure_filename(i.filename) for i in article_images if secure_filename(i.filename)]

        if article_text.count(img_tag) + article_text.count(group_img_tag) == len(name_of_article_images) or \
                (len(name_of_article_images) == 1 and name_of_article_images == [''] and
                 article_text.count(img_tag) + article_text.count(group_img_tag) ==
                 len(name_of_article_images[0])):

            name_of_article_images = load_images(article_images)

            article_info = Article(title=form.title.data.strip(),
                                   author_id=current_user.id,
                                   coords=form.coords_of_place.data,
                                   thumbnail_img=title_filename if title_filename != ''
                                   else 'https://i.imgur.com/HrLbqAM.png',
                                   text=article_text,
                                   article_imgs=', '.join(name_of_article_images),
                                   article_category_id=form.category.data)
            db.session.add(article_info)
            db.session.commit()

        else:
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert="alert alert-danger",
                                   message="Кол-во указанных изображений не соответствует загруженным",
                                   title_image_name=title_image_name,
                                   article_images=article_images, min_length_of_text=min_length_of_text,
                                   submit_button_text='Опубликовать')

        # --------------------------------------------------------------------------------

        return redirect('/')

    return render_template('Forms/article_form.html', title='Добавление статьи', form=form,
                           title_image_name=title_image_name,
                           article_images=article_images, min_length_of_text=min_length_of_text,
                           submit_button_text='Опубликовать')


# Edit article form
@article_actions.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@is_user_admin
def edit_article(article_id):
    title_image_name, article_images = 'Титульное изображение', 'Загрузить изображения'
    form = ArticleForm()

    form.category.choices = [(i.id, i.name_of_category) for i in Category.query.all()]

    if request.method == "GET":

        article_by_id = Article.query.filter(Article.id == article_id,
                                             Article.user == current_user).first()
        if article_by_id:

            form.title.data = article_by_id.title
            form.coords_of_place.data = article_by_id.coords
            form.text.data = article_by_id.text.replace('<br>', '\r')
            form.category.data = article_by_id.article_category_id
            title_image_name = article_by_id.thumbnail_img

            article_imgs = article_by_id.article_imgs.split(', ')
            length_of_article_images = len(article_imgs)

            article_images = f'{length_of_article_images} файла(ов) выбрано' if length_of_article_images > 1 \
                else article_imgs[0]

        else:
            abort(404)

    if request.method == 'POST':
        article_text = form.text.data.replace('\r', '<br>')
        if len(article_text.split()) < min_length_of_text:
            return render_template('Forms/article_form.html', title='Редактирование статьи',
                                   form=form, alert="alert alert-danger",
                                   message="Текст статьи слишком маленький", title_image_name=title_image_name,
                                   article_images=article_images, submit_button_text='Сохранить')

        # ----------------------- Formatting text for article card -----------------------

        article_info = Article.query.filter(Article.id == article_id,
                                            Article.user == current_user).first()
        if article_info:

            # Downloading title images
            list_of_title_imgs = request.files.getlist('thumbnail-img')
            title_filename = load_images(list_of_title_imgs)[0]

            # Downloading article images
            article_images = request.files.getlist('article-images')

            name_of_article_images = \
                [secure_filename(i.filename) for i in article_images if secure_filename(i.filename)]

            if not name_of_article_images:
                name_of_article_images = article_info.article_imgs.split(', ')

            if article_text.count(img_tag) + article_text.count(group_img_tag) == len(name_of_article_images) or \
                    (len(name_of_article_images) == 1 and name_of_article_images == [''] and
                     article_text.count(img_tag) + article_text.count(group_img_tag) ==
                     len(name_of_article_images[0])):

                name_of_article_images = load_images(article_images)

                article_info.title = form.title.data.strip()
                article_info.coords = form.coords_of_place.data
                article_info.thumbnail_img = title_filename.strip() if title_filename != '' \
                    else article_info.thumbnail_img
                article_info.text = article_text
                article_info.article_imgs = ', '.join(name_of_article_images)
                article_info.article_category_id = form.category.data
                db.session.add(article_info)
                db.session.commit()

            else:
                return render_template("Forms/article_form.html", title='Редактирование статьи',
                                       form=form, alert="alert alert-danger",
                                       message="Кол-во указанных изображений не соответствует загруженным",
                                       title_image_name=title_image_name,
                                       article_images=article_images, submit_button_text='Сохранить')
            # --------------------------------------------------------------------------------

            return redirect('/')

        else:
            abort(404)

    return render_template('Forms/article_form.html', title='Редактирование статьи', form=form,
                           title_image_name=title_image_name,
                           article_images=article_images, submit_button_text='Сохранить')


# Delete article
@article_actions.route('/delete_article/<int:article_id>', methods=['GET', 'POST'])
@is_user_admin
def delete_article(article_id):
    article_by_id = Article.query.filter_by(id=article_id).first()
    if article_by_id:
        db.session.delete(article_by_id)
        db.session.commit()
    else:
        abort(404)
    return redirect('/')
