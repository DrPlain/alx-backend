#!/usr/bin/env python3
""" Helper function module """


def index_range(page: int, page_size: int) -> tuple:
    """ Returns a tuple containing a start index and
    an end index corresponding to the range of indexes
    defined by page and page_size
    """

    count = 0
    idx = 0
    while True:
        if idx != 0 and idx % page_size == 0:
            count = count + 1
            if count == page:
                return (idx - page_size, idx)
        idx = idx + 1
