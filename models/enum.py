#!/usr/bin/env python3
"""Defines a set of Enum classes"""

from enum import Enum


class BaseEnum(Enum):
    """BaseEnum Class"""

    def to_dict(self, detailed=False):
        return self.value


class UserRole(BaseEnum):
    admin = "admin"
    moderator = "moderator"
    editor = "editor"
    contributor = "contributor"
    member = "member"
    user = "user"
    customer = "customer"
