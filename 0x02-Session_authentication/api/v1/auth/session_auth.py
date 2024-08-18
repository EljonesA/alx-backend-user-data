#!/usr/bin/env python3
"""
Module to manage session authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class to manage session-based authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate unique seesion ID using uuid4
        session_id = str(uuid.uuid4())

        # store the session ID & user_id mapping
        self.user_id_by_session_id[session_id] = user_id

        return session_id
