#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Uploading image to Imgur"""

from requests import post
from .const import CLIENT_ID, imgur_api_url


def upload_image(img_upload):

    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}

    image_link = post(
        imgur_api_url,
        headers=headers,
        data={
            'image': img_upload
        }
    ).json()

    return image_link['data']['link']
