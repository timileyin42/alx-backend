#!/usr/bin/env python3


"""LRUCache Module"""


from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """LRUCache class - LRU caching system"""
    def __init__(self):
        """Initialize LRUCache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lru, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {lru}")

    def get(self, key):
        """Gets item by key"""
        if key is None or key not in self.cache_data:
            return None
        u = self.cache_data.pop(key)
        self.cache_data[key] = u
        return u
