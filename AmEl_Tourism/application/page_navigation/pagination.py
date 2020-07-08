#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Implementing pagination """

from math import ceil

from flask import render_template, abort

from ..data.articles import Category
from ..extensions.const import max_num_of_articles_per_page
from ..extensions.img_tags import img_tag, group_img_tag, img_group_tag, \
    img_group_closing_tag


class PageNavigation(object):
    """ Class for creating paginated navigation """

    def __init__(self, page_id: int, category):
        self.page_id = page_id
        self.category = category

    def add_page_navigation(self, places: list, is_index: bool,
                            *category_id: int):
        """ Function for adding paginated navigation
        :param places: list of places
        :param is_index: has any category been selected
        :param category_id: optional; id of the category that the user selected
        """

        href: str = f'/page' if is_index else f'/category/{category_id[0]}/page'

        return render_template('index.html', title='AmEl Tourism',
                               places=places[max_num_of_articles_per_page *
                                             (self.page_id - 1):
                                             max_num_of_articles_per_page *
                                             self.page_id],
                               pages_info=self.pages_info(ceil(
                                   len(places) / max_num_of_articles_per_page)),
                               page_id=self.page_id, href=href,
                               category_list=self.category.query,
                               img_tag=img_tag, group_img_tag=group_img_tag,
                               img_group_tag=img_group_tag,
                               img_group_closing_tag=img_group_closing_tag)

    def pages_info(self, total: int) -> list:
        """ Return information about the location of the page relative to others
        :param total: total number of pages
        """

        # If there are no pages
        if self.page_id > total or self.page_id < 1:
            abort(404)

        pervpage, nextpage = self.checking_nav_arrows(1, '«'), \
                             self.checking_nav_arrows(total, '»')

        page1left, page1right = self.page_id - 1 \
                                    if self.page_id - 1 > 0 else '', \
                                self.page_id + 1 \
                                    if self.page_id + 1 <= total else ''

        page2left, page2right = (self.page_id - 2 if nextpage[
            -1] else 1) if self.page_id - 2 > 0 else '', \
                                (self.page_id + 2 if pervpage[-1] else total) \
                                if self.page_id + 2 <= total else ''

        filtered_list_of_pages: list = sorted(
            [i for i in
             [page2left, page1left, self.page_id, page1right, page2right] if i])
        for i, j in enumerate(filtered_list_of_pages):
            if (pervpage[-1] or nextpage[-1]) and (
                    type(j) == int and i + 1 < len(filtered_list_of_pages) and
                    j + 1 != filtered_list_of_pages[
                        i + 1]):
                filtered_list_of_pages.insert(i + 1, ('..', False))
                break

        filtered_list_of_pages.insert(0, pervpage) if pervpage else None
        filtered_list_of_pages.append(nextpage) if nextpage else None

        return [(i, True) if type(i) == int else i for i in
                [i if i != self.page_id else (self.page_id, None) for i in
                 filtered_list_of_pages]]

    def checking_nav_arrows(self, num: int, arrow: str) -> tuple:
        """ Check for nav arrows
        :param num: number to be checked
        :param arrow: arrow to be checked
        """

        return (arrow, True) if self.page_id != num else (arrow, False)
