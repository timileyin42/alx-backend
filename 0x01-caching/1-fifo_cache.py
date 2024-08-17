#!/usr/bin/env python3


"""FIFOCache Module"""


from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """FIFOCache class - FIFO caching system"""
    def __init__(self):
        """Initialize FIFOCache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            fst, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {fst}")

    def get(self, key):
        """Gets item by key"""
        return self.cache_data.get(key, None)
