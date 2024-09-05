#!/usr/bin/env python3
"""
session auth expiration module for the API
"""
from api.v1.auth.session_auth import SessionAuth
import os
import datetime
from models.user import User
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """ Class for session Auth expiry """
    def __init__(self):
        """ constructor method for session exp"""
        super().__init__()
        try:
            session_duration = int(os.getenv("SESSION_DURATION"), '0')
        except Exception:
            session_duration = 0

    def create_session(self, user_id=None):
        """ create session method """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {}
        session_dict["user_id"] = user_id
        session_dict["created_at"] = datetime.datetime.now()
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user_id for session id method """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            session_dict = self.user_id_by_session_id[session_id]
            return session_dict["user_id"]
        if "created_at" not in session_dict:
            return None
        current_time = datetime.now()
        elapsed_time = datetime.timedelta(seconds=self.session_duration)
        if session_dict["created_at"] + elapsed_time < current_time:
            return None
        return session_dict["user_id"]
