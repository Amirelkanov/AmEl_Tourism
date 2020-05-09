#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Uploading images """

from os.path import exists

from werkzeug.utils import secure_filename


def load_images(list_of_images, save_dir):
    for img_upload in list_of_images:
        article_filename = secure_filename(img_upload.filename)
        save_path = str(save_dir / article_filename)
        if not exists(save_path):
            img_upload.save(save_path)
