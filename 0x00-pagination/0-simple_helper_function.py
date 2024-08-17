#!/usr/bin/env python3
"""Defines the index_range func for pagination"""


from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate the start and end indexes for a pagination range"""
    begin, end = 0, 0
    for u in range(page):
        begin = end
        end += page_size

    return (begin, end)
