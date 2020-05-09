#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Image directories """

from pathlib import Path

IMG_DIR = '../static/img'
ARTICLE_IMG_DIR: Path = Path(__file__).parent / IMG_DIR / 'article_imgs'
TITLE_IMG_DIR: Path = Path(__file__).parent / IMG_DIR / 'title_imgs'
