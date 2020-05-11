#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle

from bs4 import BeautifulSoup
from flask import Blueprint, render_template

from ..extensions.img_tags import img_tag, group_img_tag, img_group_tag, img_group_closing_tag
from ..extensions.is_admin_decorator import is_user_admin
from ..data.articles import Article, Category
from ..page_navigation.pagination import PageNavigation

main = Blueprint('main', __name__)


# Index page
@main.route('/')
@main.route('/index')
@main.route('/page/<int:page_id>')
def index(page_id=1):
    places = Article.query.all()
    return PageNavigation(page_id, Category).add_page_navigation(places, True)


# Page showing articles by category
@main.route('/category/<int:category_id>')
@main.route('/category/<int:category_id>/page/<int:page_id>')
def articles_by_category(category_id, page_id=1):
    places = Article.query.filter_by(article_category_id=category_id).all()
    return PageNavigation(page_id, Category).add_page_navigation(places, False, category_id)


# Article page
@main.route('/article/<int:article_id>')
def article(article_id):
    related_posts = list()
    article_info = Article.query.filter_by(id=article_id).first()

    list_of_articles_by_category = \
        Article.query.filter(Article.article_category_id == article_info.article_category_id,
                             Article.id != article_info.id).all()
    shuffle(list_of_articles_by_category)

    if len(list_of_articles_by_category) >= 3:
        related_posts = list_of_articles_by_category[:3]

    rendered_page = BeautifulSoup(render_template('article.html',
                                                  title=article_info.title, article_info=article_info,
                                                  category_list=Category.query,
                                                  related_posts=related_posts), 'lxml')

    article_images, article_text = article_info.article_imgs.split(', '), article_info.text

    for i, article_img in enumerate(article_images):
        article_text.count(img_tag) + article_text.count(group_img_tag)

        image_html_tag = f'<img src="{article_img}" alt="">'

        # ----------------------- Replacing input [blocks] to <html> blocks -----------------------

        image_tag_st_ind, group_img_tag_ind = article_text.find(img_tag), article_text.find(group_img_tag)

        # Inserting single image
        if image_tag_st_ind != -1:
            article_text = article_text[
                           :image_tag_st_ind] + '<br><p class="centered-image post-format">' + \
                           f'<img src="{article_img}" alt="" ' \
                           f'class="pinit">' + '</p>' + \
                           article_text[image_tag_st_ind + len(img_tag):]

        # Inserting group image
        elif group_img_tag_ind != -1:

            article_text = article_text[:group_img_tag_ind] + \
                           f'<li class="blocks-gallery-item">{image_html_tag}</li>' + \
                           article_text[group_img_tag_ind + len(group_img_tag):]

        # Inserting image group tag
        article_text = article_text.replace(img_group_tag,
                                            '<br><p><ul class="wp-block-gallery columns-4 is-cropped">'). \
            replace(img_group_closing_tag, '</ul>')

        # -----------------------------------------------------------------------------------------

    # Inserting formatted code into div
    rendered_page.find("div", id="article_text").insert(0, article_text)

    return rendered_page.prettify().replace('&lt;', '<').replace('&gt;', '>')


# About us page
@main.route('/about')
def about_us():
    return render_template('about_us.html', title='О нас')


# Page showing categories
@main.route('/categories')
@is_user_admin
def categories():
    return render_template('Admin/categories.html', title='Категории',
                           list_of_categories=Category.query.all())
