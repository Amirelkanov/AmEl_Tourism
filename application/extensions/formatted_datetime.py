#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Formatting datetime """

from .const import RU_MONTH_VALUES


def get_formatted_datetime(datetime):
    return datetime.strftime(f'{datetime.day} {RU_MONTH_VALUES[datetime.month]} %Y %H:%M')
