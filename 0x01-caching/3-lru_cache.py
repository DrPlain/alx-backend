#!/usr/bin/env python3
"""
LRU -Least recently used cache class module
"""
from base_caching import BaseCaching
from datetime import datetime


class LRUCache(BaseCaching):
    """
    LRU cache class
    """
    key_use_frequency = {}

    def __init__(self):
        """ Class constructor """
        super().__init__()

    def put(self, key, item):
        """ Add an item to cache """
        if key and item:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS:
                self.cache_data[key] = item
                LRUCache.key_use_frequency[key] = datetime.now()
            else:
                if key in self.cache_data.keys():
                    self.cache_data[key] = item
                    LRUCache.key_use_frequency[key] = datetime.now()
                else:
                    sort_key = LRUCache.key_use_frequency.get
                    my_dict = LRUCache.key_use_frequency
                    key_least_used = min(my_dict, key=sort_key)
                    del self.cache_data[key_least_used]
                    del LRUCache.key_use_frequency[key_least_used]
                    print(f"DISCARD: {key_least_used}")

                    self.cache_data[key] = item
                    LRUCache.key_use_frequency[key] = datetime.now()

    def get(self, key):
        """ Retrieves an item from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        LRUCache.key_use_frequency[key] = datetime.now()
        return self.cache_data[key]
