#!/usr/bin/env python3
"""Basic Authentication System Module"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """A class to manage Basic Authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.removeprefix("Basic ")

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            encoded = base64.b64decode(base64_authorization_header)
            return encoded.decode("utf-8")
        except Exception as err:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if decoded_base64_authorization_header.find(":") == -1:
            return None, None
        email, password = decoded_base64_authorization_header.split(":")
        return email, password
