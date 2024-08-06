#!/usr/bin/env python3
""" Create a class BasicAuth that inherits from Auth """
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args: authorization_header (str): The authorization header.

        Returns: str: The Base64 part of the Authorization header, or
        None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header for Basic
        Authentication.

        Args: base64_authorization_header (str): The Base64 part of the
        authorization header.

        Returns: str: The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user email and password from the Base64 decoded value.

        Args: decoded_base64_authorization_header (str): The decoded
        Base64 authorization header.    

        Returns: Tuple[str, str]: The user email and password, or
        (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]
