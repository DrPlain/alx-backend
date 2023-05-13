#!/usr/bin/env python3
""" Helper function module """


def index_range(page: int, page_size: int) -> tuple:
    """ Returns a tuple containing a start index and
    an end index corresponding to the range of indexes
    defined by page and page_size
    """

    nextSartPageIndex = page * page_size
    return nextSartPageIndex - page_size, nextSartPageIndex
