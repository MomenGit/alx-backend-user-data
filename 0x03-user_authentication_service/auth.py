#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Saves a new user"""
        user = None

        try:
            user = self._db.find_user_by(email=email)
        except Exception as err:
            pass

        if user is not None:
            raise ValueError(f"User {email} already exists")

        hashed_pwd = _hash_password(password)
        new_user = self._db.add_user(email, hashed_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks that the user exists and that the password is correct"""
        try:
            user = self._db.find_user_by(email=email)
            encoded_pwd = password.encode('utf-8')

            return bcrypt.checkpw(encoded_pwd, user.hashed_password)
        except Exception as err:
            pass

        return False


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    salt = bcrypt.gensalt()
    encoded_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)
    return hashed_pwd
