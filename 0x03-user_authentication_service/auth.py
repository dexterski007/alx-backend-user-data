#!/usr/bin/env python3
"""auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash password method """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf8'), salt)
