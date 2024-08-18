#!/usr/bin/env python3
""" session db module """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB auth """
    def create_session(self, user_id=None):
        """Create and store a new UserSession"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save session to the database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID from the database based on session ID"""
        if session_id is None:
            return None

        user_session = UserSession.load(session_id=session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            user_session.delete()  # Remove expired session
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy a UserSession based on the session ID from the request
        cookie"""
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_session = UserSession.load(session_id=session_id)
        if user_session:
            user_session.delete()  # Delete session from the database
            return True

        return False
