#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt


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
