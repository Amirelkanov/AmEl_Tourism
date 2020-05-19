#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Initializing columns for tables: Articles, Categories """

from sqlalchemy_serializer import SerializerMixin

from ..extensions.init_models import db

association_table = db.Table('association', db.metadata,
                             db.Column('articles', db.Integer,
                                       db.ForeignKey('articles.id')),
                             db.Column('categories', db.Integer,
                                       db.ForeignKey('categories.id'))
                             )


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey("users.id"))
    title = db.Column(db.String, nullable=False)
    coords = db.Column(db.String, nullable=False)
    thumbnail_img = db.Column(db.String)
    article_imgs = db.Column(db.String)
    text = db.Column(db.Text, nullable=False)
    article_category_id = db.Column(db.Integer,
                                    db.ForeignKey("categories.id"))
    user = db.relation("User")
    category = db.relation("Category",
                           secondary="association",
                           backref="articles")


class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name_of_category = db.Column(db.String, nullable=False)

    user = db.relation("Article")

    category_columns_name = {
        'id': 'ID',
        'name_of_category': 'Название категории',
    }
