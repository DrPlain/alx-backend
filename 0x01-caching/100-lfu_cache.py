#!/usr/bin/env python3
"""
LRU -Least recently used cache class module
"""
from base_caching import BaseCaching
from datetime import datetime


class LFUCache(BaseCaching):
    """
    LRU cache class
    """
    key_use_datetime = {}
    key_use_frequency = {}

    def __init__(self):
        """ Class constructor """
        super().__init__()

    def put(self, key, item):
        """ Add an item to cache """
        if key and item:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS:
                self.cache_data[key] = item
                LFUCache.key_use_datetime[key] = datetime.now()
                LFUCache.key_use_frequency[key] = 0
            else:
                if key in self.cache_data.keys():
                    self.cache_data[key] = item
                    LFUCache.key_use_datetime[key] = datetime.now()
                    LFUCache.key_use_frequency[key] = 0
                else:
                    sort_key_accessed = LFUCache.key_use_datetime.get
                    my_dict_accessed = LFUCache.key_use_datetime
                    key_least_accessed = min(
                        my_dict_accessed, key=sort_key_accessed)
                    sorted_frequency = sorted(
                        LFUCache.key_use_frequency.values())
                    min_frequency = sorted_frequency[0]
                    frequency_dict = LFUCache.key_use_frequency.copy()
                    key_min = []
                    for k, v in frequency_dict.items():
                        if v == min_frequency:
                            key_min.append(k)
                    if len(key_min) == 1:
                        del self.cache_data[key_min[0]]
                        del LFUCache.key_use_datetime[key_min[0]]
                        del LFUCache.key_use_frequency[key_min[0]]
                        print(f"DISCARD: {key_min[0]}")
                    elif len(key_min) > 1:
                        for k in key_min:
                            if k == key_least_accessed:
                                del self.cache_data[k]
                                del LFUCache.key_use_datetime[k]
                                del LFUCache.key_use_frequency[k]
                                print(f"DISCARD: {k}")

                    self.cache_data[key] = item
                    LFUCache.key_use_datetime[key] = datetime.now()
                    LFUCache.key_use_frequency[key] = 0

    def get(self, key):
        """ Retrieves an item from cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        LFUCache.key_use_datetime[key] = datetime.now()
        LFUCache.key_use_frequency[key] += 1
        return self.cache_data[key]
