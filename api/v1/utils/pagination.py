#!/usr/bin/env python3
"""
Pagination processing module, this function is written to be
used in a flask application... using it outside flask will resolve
to exceptions being raised.
"""
from os import getenv
from flask import request
from typing import Dict, Callable
from math import ceil

PAGINATION = int(getenv('PAGINATION', 25))


def pagination(items: list, request=request,
               func: Callable = None, size=PAGINATION,
               sort: bool = True) -> Dict[str, any]:
    """Divide items into pages and returned the data"""

    if not hasattr(items, '__iter__'):
        raise TypeError('Expects items to be an iterable.')
    items = list(items)
    if sort:
        items = sorted(items, key=lambda x: x.created_at, reverse=True)

    total_pages = ceil(len(items) / size)
    total_items = len(items)
    try:
        page = int(request.args.get('page', 1))
        if page <= 0:
            page = 1
    except ValueError:
        if request.args.get('page') == 'all':
            return {
                "page": 1,
                "page_size": total_items,
                "total_items": total_items,
                "total_pages": 1,
                "items": items if func is None else [func(x) for x in items]
            }
        else:
            page = 1

    items = items[(page - 1) * size: page * size]
    page_size = len(items)

    return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "items": items if func is None else [func(x) for x in items]
    }
