#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Uploading images """

from os import path, remove

import pyimgur
from werkzeug.utils import secure_filename

from .const import CLIENT_ID, SAVE_DIR


def load_images(list_of_images):
    im = pyimgur.Imgur(CLIENT_ID)
    links = []
    for img_upload in list_of_images:
        article_filename = secure_filename(img_upload.filename)
        save_path = SAVE_DIR + article_filename
        if not path.exists(save_path):
            img_upload.save(save_path)
            links.append(im.upload_image(save_path).link)
            remove(save_path)
    return links if len(links) > 0 else ['']
