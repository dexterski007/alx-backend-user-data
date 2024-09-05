#!/usr/bin/env python3
"""
session auth expiration module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os
from datetime import datetime, timedelta
from models.user import User
from uuid import uuid4

format = "%Y-%m-%dT%H:%M:%S"


class SessionDBAuth(SessionExpAuth):
    """ Class for session Auth db """
    def create_session(self, user_id=None):
        """ create session method """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.now().strftime(format)
        }
        session = UserSession(**kwargs)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session db """
        if session_id is None:
            return None
        try:
            session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if session is None:
            return None
        if self.session_duration > 0:
            if (datetime.now() - session[0].created_at)\
                 .total_seconds() > self.session_duration:
                return None
        return session[0].user_id

    def destroy_session(self, request=None):
        """ destroy session method """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            session = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        session[0].remove()
        return True
