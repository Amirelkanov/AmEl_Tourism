#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Pages for all users """

from random import shuffle

from bs4 import BeautifulSoup
from flask import Blueprint, render_template

from ..data.articles import Article, Category
from ..extensions.const import YANDEX_API_KEY
from ..extensions.img_tags import img_tag, group_img_tag, img_group_tag, \
    img_group_closing_tag
from ..extensions.lonlat_converting import lonlat_to_bounds
from ..page_navigation.pagination import PageNavigation

# Main Blueprint registration
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@main.route('/page/<int:page_id>')
def index(page_id: int = 1):
    """ Index page
    :param page_id: which page is the user on
    """

    places = Article.query.all()
    return PageNavigation(page_id, Category).add_page_navigation(places, True)


@main.route('/category/<int:category_id>')
@main.route('/category/<int:category_id>/page/<int:page_id>')
def articles_by_category(category_id: int, page_id: int = 1):
    """ Showing articles by category
    :param category_id: which category (or more precisely, id) the user selected
    :param page_id: which page is the user on
    """

    places = Article.query.filter_by(article_category_id=category_id).all()
    return PageNavigation(page_id, Category).add_page_navigation(places, False,
                                                                 category_id)


@main.route('/article/<int:article_id>')
def article(article_id: int) -> str:
    """ Showing article
    :param article_id: the article (or more precisely, the id)
    that the user is on
    """

    article_info = Article.query.filter_by(id=article_id).first()

    # Creating "Related posts"
    list_of_articles_by_category: list = \
        Article.query.filter(
            Article.article_category_id == article_info.article_category_id,
            Article.id != article_info.id).all()
    shuffle(list_of_articles_by_category)
    related_posts: list = list_of_articles_by_category[:3] if len(
        list_of_articles_by_category) >= 3 else []

    article_template = render_template('article.html',
                                       title=article_info.title,
                                       article_info=article_info,
                                       category_list=Category.query,
                                       api_key=YANDEX_API_KEY,
                                       bounds_of_place=lonlat_to_bounds(
                                           article_info.coords.split(', ')),
                                       related_posts=related_posts)
    rendered_page = BeautifulSoup(article_template, 'lxml')

    article_images, article_text = article_info.article_imgs.split(
        ', '), article_info.text

    # --------------- Replacing input [blocks] to <html> blocks ---------------

    for i, article_img in enumerate(article_images):

        image_tag_st_ind, group_img_tag_ind = article_text.find(img_tag),\
                                              article_text.find(group_img_tag)

        # Inserting single image
        if image_tag_st_ind != -1:
            article_text = f"""{article_text[:image_tag_st_ind]} <br><p class="
centered-image post-format"><img src="{article_img}" alt="" class="pinit"></p> {
            article_text[image_tag_st_ind + len(img_tag):]}"""

        # Inserting group image
        elif group_img_tag_ind != -1:
            article_text = f"""{article_text[:group_img_tag_ind]} <li class="
blocks-gallery-item"><img src="{article_img}" alt=""></li>{
            article_text[group_img_tag_ind + len(group_img_tag):]}"""

        # Inserting image group tag
        article_text: str = article_text.replace(
            img_group_tag,
            '<br><p><ul class="wp-block-gallery columns-4 is-cropped">'). \
            replace(img_group_closing_tag, '</ul>')

    # -------------------------------------------------------------------------

    # Inserting formatted code into div
    rendered_page.find("div", id="article_text").insert(0, BeautifulSoup(
        article_text, 'lxml'))
    return str(rendered_page)


# About us page
@main.route('/about')
def about_us():
    return render_template('about_us.html', title='О нас')
