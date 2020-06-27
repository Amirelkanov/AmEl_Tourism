#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import post

from .const import CLIENT_ID, imgur_api_url


def upload_image(img_upload: bytes) -> str:
    """ Image upload to hosting
    :param img_upload: byte image to upload
    """

    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}

    image_link: dict = post(
        imgur_api_url,
        headers=headers,
        data={
            'image': img_upload
        }
    ).json()

    return image_link['data']['link']
