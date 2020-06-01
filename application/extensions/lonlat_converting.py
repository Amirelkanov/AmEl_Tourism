#!/usr/bin/python
# -*- coding: utf-8 -*-

from .const import lonlat_factor


def lonlat_to_bounds(lonlat):
    return str(
        [[round(eval(f'{j} {sign} {lonlat_factor[i]}'), 6) for i, j in enumerate(lonlat)] for sign in
         ['-', '+']]).replace(', [', ',[')
