#!/usr/bin/env python3
"""
MRU -Most recently used cache class module
"""
from base_caching import BaseCaching
from datetime import datetime


class MRUCache(BaseCaching):
    """
    MRU cache class
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
                MRUCache.key_use_frequency[key] = datetime.now()
            else:
                if key in self.cache_data.keys():
                    self.cache_data[key] = item
                    MRUCache.key_use_frequency[key] = datetime.now()
                else:
                    sort_key = MRUCache.key_use_frequency.get
                    my_dict = MRUCache.key_use_frequency
                    key_most_recently_used = max(my_dict, key=sort_key)
                    del self.cache_data[key_most_recently_used]
                    del MRUCache.key_use_frequency[key_most_recently_used]
                    print(f"DISCARD: {key_most_recently_used}")

                    self.cache_data[key] = item
                    MRUCache.key_use_frequency[key] = datetime.now()

    def get(self, key):
        """ Retrieves an item from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        MRUCache.key_use_frequency[key] = datetime.now()
        return self.cache_data[key]
