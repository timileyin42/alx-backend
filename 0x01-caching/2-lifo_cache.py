#!/usr/bin/env python3


"""Last In First Out Cache Module"""


from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache class - LIFO caching system"""
    def __init__(self):
        """Initialize LIFOCache"""
        super().__init__()

    def put(self, key, item):
        """Adds item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lst = list(self.cache_data.keys())[-2]
            del self.cache_data[lst]
            print(f"DISCARD: {lst}")

    def get(self, key):
        """Gets item by key"""
        return self.cache_data.get(key, None)
