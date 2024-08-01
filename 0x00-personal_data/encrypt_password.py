#!/usr/bin/env python3
""" Password encryption using bcrypt
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password using bcrypt """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validate a password against a hashed password """
    return bcrypt.checkpw(password.encode(), hashed_password)
