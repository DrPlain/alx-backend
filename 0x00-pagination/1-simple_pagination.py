#!/usr/bin/env python3
""" Simple Pagination """
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """ Returns a tuple containing a start index and
    an end index corresponding to the range of indexes
    defined by page and page_size
    """

    nextSartPageIndex = page * page_size
    return nextSartPageIndex - page_size, nextSartPageIndex


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = index_range(page, page_size)
        try:
            data = self.dataset()
            return data[start:end]
        except IndexError:
            return []