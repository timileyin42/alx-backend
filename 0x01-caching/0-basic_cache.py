#!/usr/bin/env python3


"""BasicCache Module"""


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class - Basic caching system"""
    def put(self, key, item):
        """Adds item in the cache"""
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """Gets item by key"""
        return self.cache_data.get(key, None)
