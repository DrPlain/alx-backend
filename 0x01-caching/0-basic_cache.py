#!/usr/bin/env python3
""" Basic dictionary caching """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ Basic cache class """

    def __init__(self):
        """ constructor """
        super().__init__()

    def put(self, key, item):
        """ Adds to the caching dictionary """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Gets a cached data with a key """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
