#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password, salt)
    return hashed_pwd
