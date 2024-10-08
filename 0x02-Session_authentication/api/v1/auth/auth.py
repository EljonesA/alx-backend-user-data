#!/usr/bin/env python3
"""
Module to manage API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Manages API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required """
        # case 1: if path is None, authentication is required
        if path is None:
            return True

        # Case 2: If excluded_paths is None/empty, authentication required
        if not excluded_paths:
            return True

        # Normalize path and excluded_paths by stripping trailing slashes
        normalized_path = path.rstrip('/')
        normalized_excluded_paths = [p.rstrip('/') for p in excluded_paths]

        # case 3: if path is in excluded_paths, auth not required
        if normalized_path in normalized_excluded_paths:
            return False

        # Other cases, authentication required
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None

    def session_cookie(self, request=None) -> str:
        """ Returns the session cookie value from the request """
        if request is None:
            return None

        # Get the cookie name from the environment variable
        cookie_name = getenv("SESSION_NAME", "_my_session_id")

        # Return the value of the specified cookie from the request
        return request.cookies.get(cookie_name)
