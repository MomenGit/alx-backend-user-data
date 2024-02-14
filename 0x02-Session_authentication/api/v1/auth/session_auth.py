#!/usr/bin/env python3
"""Session Authentication System Module"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Class that manages Session Authentication"""

    def __init__(self) -> None:
        self.user_id_by_session_id = {}
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4().__str__()
        self.user_id_by_session_id.__setitem__(session_id, user_id)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
