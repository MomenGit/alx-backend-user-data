#!/usr/bin/env python3
"""Module template for all authentication system"""
from flask import request
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
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Check Authorization header"""
        if request is None:
            return None
        if request.authorization is None:
            return None

        return request.authorization.to_header()

    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
