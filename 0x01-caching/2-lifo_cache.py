#!/usr/bin/env python3
""" LIFOCache class """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO Cache class """
    track_key = []

    def __init__(self):
        """ class constructor """
        super().__init__()

    def put(self, key, item):
        """ Adds an item to cache """
        if key and item:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS:
                self.cache_data[key] = item
                LIFOCache.track_key.append(key)
            else:
                if key in self.cache_data.keys():
                    self.cache_data[key] = item
                    LIFOCache.track_key.append(key)
                else:
                    last_key = LIFOCache.track_key[-1]
                    del self.cache_data[last_key]
                    self.cache_data[key] = item
                    LIFOCache.track_key.append(key)
                    print(f"DISCARD: {last_key}")

    def get(self, key):
        """ Gets a value from cache """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
