#!/usr/bin/env python3
"""
Module to manage session authentication
"""
from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from os import getenv
from models.user import User


class SessionAuth(Auth):
    """Session authentication class to manage session-based authentication"""
    # user_id_by_session_id = {}
    def __init__(self):
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate unique seesion ID using uuid4
        session_id = str(uuid.uuid4())

        # store the session ID & user_id mapping
        self.user_id_by_session_id[session_id] = user_id
        print(f"Session created: {session_id} for user {user_id}")

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None

        # return user ID associated with the session ID
        user_id = self.user_id_by_session_id.get(session_id)
        print(f"User ID for session {session_id}: {user_id}")
        return user_id

    def session_cookie(self, request=None) -> str:
        """ Returns the session cookie value from the request """
        if request is None:
            return None
        cookie_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the User instance based on the session cookie """
        if request is None:
            return None

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)
        print(f"Session ID from cookie: {session_id}")
        if session_id is None:
            return None

        # Get the user ID based on the session ID
        user_id = self.user_id_for_session_id(session_id)
        print(f"User ID from session ID: {user_id}")
        if user_id is None:
            return None

        # Retrieve the User instance from the database
        print(f"User retrieved from database: {User.get(user_id)}")
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy a session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete the session
        del self.user_id_by_session_id[session_id]
        return True
