#!/usr/bin/env python3
"""Defines User class"""

from typing import Dict
from models.base_model import Base, BaseModel
from sqlalchemy import (
    Column, String, Enum, DateTime, Boolean, Text
)
from models.user.auth import UserAuth
from models.enum import UserRole
from datetime import datetime


class User(BaseModel, Base, UserAuth):
    """User class"""
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    address = Column(String(500))
    image = Column(Text)
    role = Column(Enum(UserRole), default=UserRole.user,
                  nullable=False)
    is_active = Column(Boolean, default=True)
    last_session = Column(DateTime, default=datetime.now)

    def to_dict(self, detailed=False) -> Dict[str, str]:
        """Overrides parent's defualt"""
        obj = super().to_dict()

        # attributes with their own to_dict() methods
        attrs = ['role']
        for attr in attrs:
            if hasattr(self, attr):
                if getattr(self, attr, None) is not None:
                    obj.update({attr: getattr(self, attr).to_dict()})
                else:
                    obj.update({attr: getattr(self, attr)})

        # heldback attributes
        attrs = ['_password', 'reset_token']
        for attr in attrs:
            if attr in obj:
                obj.pop(attr)

        if detailed is True:
            return obj

        # detailed attributes
        attrs = ['created_at', 'updated_at', 'email',
                 'phone', 'address', 'last_session', 'image']
        for attr in attrs:
            if attr in obj:
                obj.pop(attr)

        return obj
