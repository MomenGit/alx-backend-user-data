#!/usr/bin/env python3
"""Module template for all authentication system"""
from os import getenv
from typing import List, TypeVar


class Auth:
    """A class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Define which routes don't need authentication
        Returns True if the path is not in the list of strings excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path = path+'/'

        for exclusion in excluded_paths:
            if exclusion.endswith('*'):
                asterisk_i = exclusion.rfind('*')
                if path[:asterisk_i] == exclusion[:-1]:
                    return False

        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Check Authorization header"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
