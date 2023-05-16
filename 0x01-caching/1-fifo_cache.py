#!/usr/bin/env python3
""" FIFOCache class """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching class """

    def __init__(self):
        """ class contructor """
        super().__init__()

    def put(self, key, item):
        """ Adds an item to cache """
        if key and item:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS:
                self.cache_data[key] = item
            else:
                if key in self.cache_data.keys():
                    self.cache_data[key] = item
                else:
                    first_key = next(iter(self.cache_data.keys()))
                    del self.cache_data[first_key]
                    self.cache_data[key] = item
                    print(f"DISCARD: {first_key}")

    def get(self, key):
        """ Gets an item from cache """

        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
