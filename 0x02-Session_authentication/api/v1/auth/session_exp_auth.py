#!/usr/bin/env python3
"""
session auth expiration module for the API
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from models.user import User
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """ Class for session Auth expiry """
    def __init__(self):
        """ constructor method for session exp"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session method """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user_id for session id method """
        if session_id is None:
            return None
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict["user_id"]
            if "created_at" not in session_dict:
                return None
            current_time = datetime.now()
            elapsed_time = timedelta(seconds=self.session_duration)
            if session_dict["created_at"] + elapsed_time < current_time:
                return None
            return session_dict["user_id"]
