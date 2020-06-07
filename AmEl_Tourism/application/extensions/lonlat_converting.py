#!/usr/bin/python
# -*- coding: utf-8 -*-

from .const import lonlat_factor


def lonlat_to_bounds(lonlat: list) -> str:
    """ Converting lonlat coords to bounds
    :param lonlat: coords like "['12.345678', '12.345678']"
    """
    return str([[round(eval(f'{j} {sign} {lonlat_factor[i]}'), 6)
                 for i, j in enumerate(lonlat)] for sign in ['-', '+']]).replace(', [', ',[')
