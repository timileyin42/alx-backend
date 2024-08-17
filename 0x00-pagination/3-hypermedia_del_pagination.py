#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""


import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Retrieves info about a page from a given index"""
        data = self.indexed_dataset()
        assert index is not None and index >= 0 and index <= max(data.keys())

        pg_data = []
        num = 0
        ni = None
        start = index if index is not None else 0

        for u in range(start, len(data)):
            if u in data:
                if num < page_size:
                    pg_data.append(data[u])
                    num += 1
                else:
                    ni = u
                    break

        if num < page_size:
            ni = None

        pg_info = {
            'index': index,
            'next_index': ni,
            'page_size': len(pg_data),
            'data': pg_data,
        }
        return pg_info
