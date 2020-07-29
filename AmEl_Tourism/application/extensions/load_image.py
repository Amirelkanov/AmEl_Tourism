#!/usr/bin/python
# -*- coding: utf-8 -*-


import base64

from requests import post

from .const import CLIENT_ID, imgbb_api_url


def upload_image(img_upload: bytes) -> str:
    """ Image upload to hosting
    :param img_upload: byte image to upload
    """

    image_link: dict = post(
        imgbb_api_url,
        data={
            "key": CLIENT_ID,
            "image": base64.b64encode(img_upload)
        }
    ).json()

    return image_link["data"]["url"]
