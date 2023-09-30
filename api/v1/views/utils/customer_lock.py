#!/usr/bin/env python3
"""Customer Lock Module"""
from flask import g, abort
from functools import wraps


def customer_lock():
    """Customer Lock Wrapper"""

    def lock_wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            def denied():
                abort(401)

            customer = g.customer
            if customer is None:
                return denied()
            return f(*args, **kwargs)
        return decorated_function
    return lock_wrapper
