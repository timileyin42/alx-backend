#!/usr/bin/env python3


"""LFUCache Module"""


from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """Class implements a LFU caching system"""
    def __init__(self):
        """Initialization"""
        super().__init__()
        self.frequency = defaultdict(int)
        self.usage = OrderedDict()

    def put(self, key, item):
        """
        Cache a key-value pair.
        Evicts LFU items if cache exceeds maximum capacity.
        """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            freq_u = min(self.frequency.values())
            freq_k = [u for u, v in self.frequency.items() if v == freq_u]

            if len(freq_k) > 1:
                l_rf = {
                    u: idx for idx, u in enumerate(self.usage) if u in freq_k
                }
                rmv_k = min(l_rf, key=l_rf.get)
            else:
                rmv_k = freq_k[0]

            print(f"DISCARD: {rmv_k}")
            del self.cache_data[rmv_k]
            del self.frequency[rmv_k]
            self.usage.pop(rmv_k)

        if key in self.cache_data:
            self.usage.pop(key)
        self.usage[key] = None
        self.frequency[key] += 1
        self.cache_data[key] = item

    def get(self, key):
        """
        Gets value linked to given key, or None if key not found.
        Update usage and frequency for accessed key.
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage.pop(key)
        self.usage[key] = None
        self.frequency[key] += 1
        return self.cache_data[key]
