#!/usr/bin/env python3
"""Authentication"""
from os import getenv

AUTH_TOKEN_NAME_ON_HEADER = getenv('AUTH_TOKEN_NAME_ON_HEADER', 'x-token')
AUTH_TTL = getenv('AUTH_TTL', 259200)


class Auth:
    """A base class for other types of Auth"""
    pass
