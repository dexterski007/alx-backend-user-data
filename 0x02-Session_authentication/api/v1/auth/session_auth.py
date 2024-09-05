#!/usr/bin/env python3
"""
session auth module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Class for session Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session method """
        if user_id is None:
            return None
        if not type(user_id) is str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user id by session method """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ current user method """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ method to delete a session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            self.user_id_by_session_id.pop(session_id)
        return True
