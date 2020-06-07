#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Article related actions """

from flask import Blueprint, render_template, redirect, request, abort
from flask_login import current_user

from ....data.articles import Category, Article
from ....extensions.const import min_length_of_text
from ....extensions.img_tags import img_tag, group_img_tag
from ....extensions.init_models import db
from ....extensions.is_admin_decorator import is_user_admin
from ....extensions.load_image import upload_image
from ....forms.admin_forms import ArticleForm

# Article actions Blueprint registration
article_actions = Blueprint('article_actions', __name__)


# Article add form
@article_actions.route('/add_article', methods=['GET', 'POST'])
@is_user_admin
def add_article():
    title_image_name, article_images = 'Титульное изображение', 'Загрузить изображения'
    form = ArticleForm()

    # Choices for category select
    form.category.choices = [(i.id, i.name_of_category) for i in Category.query.all()]

    if request.method == 'POST':
        is_alert_hidden: bool = False
        article_text: str = form.text.data.replace('\r', '<br>')

        if len(article_text.split()) < min_length_of_text:
            # ERROR: The article text is too small
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert_class='alert-danger', is_alert_hidden=is_alert_hidden,
                                   message="Текст статьи слишком маленький", title_image_name=title_image_name,
                                   article_images=article_images, min_length_of_text=min_length_of_text,
                                   submit_button_text='Опубликовать')

        # WARNING: Coords format is invalid
        try:
            coords_of_place = list(map(float, form.coords_of_place.data.split(', ')))
        except ValueError:
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert_class='alert-warning', is_alert_hidden=is_alert_hidden,
                                   message="Формат координат должен быть следующим: 12.345678, 12.345678",
                                   title_image_name=title_image_name, article_images=article_images,
                                   min_length_of_text=min_length_of_text, submit_button_text='Опубликовать')

        # ----------------------- Formatting article text -----------------------

        # Downloading images
        title_img, list_of_article_images = request.files.getlist('thumbnail-img')[0].read(), [i.read() for i in
                                                                                               request.files.getlist(
                                                                                                   'article-images')]

        article_images_count: int = len(list_of_article_images) if list_of_article_images[0] else 0

        if article_text.count(img_tag) + article_text.count(group_img_tag) == article_images_count:

            # Adding and committing changes to the DB
            title_image: str = upload_image(title_img) if title_img else 'https://i.imgur.com/HrLbqAM.png'  # 404 image
            article_images: str = ', '.join([upload_image(i) for i in list_of_article_images]) \
                if list_of_article_images[0] else ''

            article_info = Article(title=form.title.data.strip(),
                                   author_id=current_user.id,
                                   coords=f'{coords_of_place[0]}, {coords_of_place[-1]}',
                                   thumbnail_img=title_image,
                                   text=article_text,
                                   article_imgs=article_images,
                                   article_category_id=form.category.data)
            db.session.add(article_info)
            db.session.commit()

        else:
            # ERROR: The number of specified images does not match the uploaded ones
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert_class='alert-danger', is_alert_hidden=is_alert_hidden,
                                   message="Кол-во указанных изображений не соответствует загруженным",
                                   title_image_name='Титульное изображение',
                                   article_images='Загрузить изображения', min_length_of_text=min_length_of_text,
                                   submit_button_text='Опубликовать')

        # --------------------------------------------------------------------------------

        return redirect('/')

    return render_template('Forms/article_form.html', title='Добавление статьи', form=form,
                           title_image_name=title_image_name, alert_class='alert-danger', is_alert_hidden=True,
                           article_images=article_images, min_length_of_text=min_length_of_text,
                           submit_button_text='Опубликовать')


@article_actions.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
@is_user_admin
def edit_article(article_id):
    """ Edit article form
    :param article_id: article (or rather, its id) to edit
    """

    title_image_name, article_images = 'Титульное изображение', 'Загрузить изображения'
    form = ArticleForm()

    # Choices for category select
    form.category.choices = [(i.id, i.name_of_category) for i in Category.query.all()]

    if request.method == "GET":

        article_by_id = Article.query.filter(Article.id == article_id,
                                             Article.user == current_user).first()
        if article_by_id:

            # Adding data from the database to forms data
            form.title.data = article_by_id.title
            form.coords_of_place.data = article_by_id.coords
            form.text.data = article_by_id.text.replace('<br>', '\r')
            form.category.data = article_by_id.article_category_id
            title_image_name = article_by_id.thumbnail_img
            article_imgs = article_by_id.article_imgs.split(', ')

            length_of_article_images: int = len(article_imgs)

            # Updating article images label text
            if length_of_article_images > 1:
                article_images = f'{length_of_article_images} файла(ов) выбрано'
            else:
                if article_imgs[0]:
                    article_images = article_imgs[0]

        else:
            abort(404)

    if request.method == 'POST':

        article_text, is_alert_hidden = form.text.data.replace('\r', '<br>'), False

        if len(article_text.split()) < min_length_of_text:
            # ERROR: The article text is too small
            return render_template('Forms/article_form.html', title='Редактирование статьи',
                                   form=form, alert_class='alert-danger', is_alert_hidden=is_alert_hidden,
                                   message="Текст статьи слишком маленький", title_image_name=title_image_name,
                                   article_images=article_images, submit_button_text='Сохранить')

        # WARNING: Coords format is invalid
        try:
            coords_of_place = list(map(float, form.coords_of_place.data.split(', ')))
        except ValueError:
            return render_template("Forms/article_form.html", title='Добавление статьи',
                                   form=form, alert_class='alert-warning', is_alert_hidden=is_alert_hidden,
                                   message="Формат координат должен быть следующим: 12.345678, 12.345678",
                                   title_image_name=title_image_name, article_images=article_images,
                                   min_length_of_text=min_length_of_text, submit_button_text='Опубликовать')

        # ----------------------- Formatting text for article card -----------------------

        article_info = Article.query.filter(Article.id == article_id,
                                            Article.user == current_user).first()
        if article_info:

            # Downloading images
            title_img, list_of_article_images = request.files.getlist('thumbnail-img')[0].read(), \
                                                [i.read() for i in request.files.getlist('article-images')]

            article_images_count = len(list_of_article_images) if list_of_article_images[0] else len(
                article_info.article_imgs.split(', ')) if article_info.article_imgs else 0

            if article_text.count(img_tag) + article_text.count(group_img_tag) == article_images_count:

                # Adding and committing changes to the DB
                title_image = upload_image(title_img) if title_img else article_info.thumbnail_img
                article_images = [upload_image(i) for i in list_of_article_images] \
                    if list_of_article_images[0] else article_info.article_imgs.split(', ')

                article_info.title = form.title.data.strip()
                article_info.coords = f'{coords_of_place[0]}, {coords_of_place[-1]}'
                article_info.thumbnail_img = title_image
                article_info.text = article_text
                article_info.article_imgs = ', '.join(article_images)
                article_info.article_category_id = form.category.data
                db.session.add(article_info)
                db.session.commit()

            else:
                # ERROR: The number of specified images does not match the uploaded ones
                return render_template("Forms/article_form.html", title='Редактирование статьи',
                                       form=form, alert_class='alert-danger', is_alert_hidden=is_alert_hidden,
                                       message="Кол-во указанных изображений не соответствует загруженным",
                                       title_image_name=article_info.thumbnail_img,
                                       article_images='Загрузить изображения', submit_button_text='Сохранить')
            # --------------------------------------------------------------------------------

            return redirect('/')

        else:
            abort(404)

    return render_template('Forms/article_form.html', title='Редактирование статьи', form=form,
                           title_image_name=title_image_name, alert_class='alert-danger', is_alert_hidden=True,
                           article_images=article_images, submit_button_text='Сохранить')


@article_actions.route('/delete_article/<int:article_id>', methods=['GET', 'POST'])
@is_user_admin
def delete_article(article_id):
    """ Deleting article
        :param article_id: article (or rather, its id) to delete
    """

    article_by_id = Article.query.filter_by(id=article_id).first()
    if article_by_id:
        # Removing an article from the database
        db.session.delete(article_by_id)
        db.session.commit()
    else:
        abort(404)
    return redirect('/')
