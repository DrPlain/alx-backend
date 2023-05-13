#!/usr/bin/env python3
""" Simple Pagination """
import csv
from typing import List, Tuple


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

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple[int, int]:
        """ Returns a tuple containing a start index and
        an end index corresponding to the range of indexes
        defined by page and page_size
        """

        nextSartPageIndex = page * page_size
        return nextSartPageIndex - page_size, nextSartPageIndex

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Gets a requested page """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = self.index_range(page, page_size)
        data = self.dataset()
        return data[start:end]
