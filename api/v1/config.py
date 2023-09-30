#!/usr/bin/env python3
"""Flask Application Config"""
from models.enum import UserRole
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.cookie_auth import CookieAuth
from api.v1.auth.jwt import JWT
from os import getenv
from models import redis

AUTH_TOKEN_NAME_ON_HEADER = getenv(
    'AUTH_TOKEN_NAME_ON_HEADER', 'x-token'
)


class AppConfig:
    USER_ROLES = list(UserRole)
    AUTH = {
        'cookie': CookieAuth(),
        'token': SessionAuth(redis=redis),
        'jwt': JWT(secret_key=getenv('API_SECRET_KEY', '#hj8i-s0jjsndu2')),
    }[getenv('AUTH_TYPE')]
    SECRET_KEY = getenv('API_SECRET_KEY')
    SWAGGER = {
        'title': 'Python Flasgger Flask API Docs',
        'description': "This is a comprehensive boilerplate project that combines Python's Flask framework and the Flasgger library to simplify the process of creating interactive API documentation for Flask-based web applications. This repository provides a starting point for developers looking to build RESTful APIs with Flask while seamlessly generating interactive Swagger-based documentation to enhance API understanding and testing.\n\nThis project is built using Python Flask, ensured to have python3 and python3-pip installed and optionally python3-venv. Depending on your OS, read how to install these packages on your Machince. \n\n`[NB: protected routes are opened in testing except routes bounded to a user specific actions]`",
        'hide_top_bar': True,
        'specs_route': '/v1/docs',
        'securityDefinitions': {
            'Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': AUTH_TOKEN_NAME_ON_HEADER,
            }
        },
        'security': [
            {
                'ApiKeyAuth': []  # Security scheme name and optional scope
            }
        ]
    }
