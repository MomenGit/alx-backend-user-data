#!/usr/bin/env python3
"""Encrypted Passwords Module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    pw_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(pw_bytes, salt)
    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password"""
    pw_bytes = password.encode()
    valid = bcrypt.checkpw(pw_bytes, hashed_password)
    return valid
