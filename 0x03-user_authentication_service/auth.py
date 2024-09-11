#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ hash password method """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf8'), salt)


def _generate_uuid() -> str:
    """ method for generating uuid """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ method for validating login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ create session method """
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user from session id """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy session method """
        user = self._db.find_user_by(user_id=user_id)
        self._db.update_user(user, session_id=None)
