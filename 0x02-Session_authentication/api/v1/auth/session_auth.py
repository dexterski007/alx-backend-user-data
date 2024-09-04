#!/usr/bin/env python3
"""
session auth module for the API
"""
from api.v1.auth.auth import Auth
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
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user id by session method """
        if session_id is None:
            return None
        if not type(session_id) is str:
            return None
        return self.user_id_by_session_id.get(session_id)
