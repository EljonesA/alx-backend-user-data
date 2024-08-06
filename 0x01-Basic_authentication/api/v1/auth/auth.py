#!/usr/bin/env python3
"""
Module to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None
