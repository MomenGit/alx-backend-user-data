#!/usr/bin/env python3
"""Authentication Module"""
from typing import Optional
from uuid import uuid4
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

    def create_session(self, email: str) -> str:
        """Creates User's session"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception as err:
            pass

        return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Returns the corresponding User for the session_id or None
        Args:
            session_id (str): user's session id
        """
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                if user is not None:
                    return user
            except Exception as err:
                pass

        return None

    def destroy_session(self, user_id: int) -> None:
        """Removes User's session
        Args:
            user_id (int): the id for the user associated with a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception as err:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Sets a user's reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception as err:
            raise ValueError

        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password after verifying reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception as err:
            raise ValueError

        self._db.update_user(user.id,
                             hashed_password=_hash_password(password))


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    salt = bcrypt.gensalt()
    encoded_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """Return a string representation of a new UUID"""
    return uuid4().__str__()
