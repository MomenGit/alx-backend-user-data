#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password"""
    salt = bcrypt.gensalt()
    encoded_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)
    return hashed_pwd
