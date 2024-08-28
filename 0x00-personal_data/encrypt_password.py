#!/usr/bin/env python3
""" function to encrypt passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ function for password hashing using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ function to check if a hash is a valid bcrypt password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
