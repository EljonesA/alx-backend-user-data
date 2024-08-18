#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args: password (str) - The password to hash.

    Returns: bytes - The salted hash of the password.
    """
    # convert password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns: User - The User object created

        Raises: ValueError - If a user with the given email already exists.
        """
        try:
            # check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, create a new one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            # find user by email
            user = self._db.find_user_by(email=email)
            # validate provided password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user.

        Args: email - email of user to create session for

        Returns: str - The session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a user by their session ID."""
        if session_id is None:
            return None

        try:
            # find user by session ID
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for a user by setting their session ID to None.
        """
        try:
            # find user by user_id
            user = self._db.find_user_by(user_id=user_id)
            # update user's session ID to none
            self._db.update_user_session(user_id=user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the user with the given email.

        Args: email - email for user

        Returns: str - resre token for the user

        Raises: ValueError - if no user with given email exists
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

        reset_token = str(uuid.uuid4())
        self._db.update_user_reset_token(user.id, reset_token)

        return reset_token
