#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash password method """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ constructor method for auth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user method"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed = _hash_password(password)
            updated = self._db.add_user(email, hashed)
            return updated
