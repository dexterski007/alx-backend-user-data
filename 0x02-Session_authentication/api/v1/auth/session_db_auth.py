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


class SessionDBAuth(SessionExpAuth):
    """ Class for session Auth db """
    def create_session(self, user_id=None):
        """ create session method """
        session_id = super().create_session(user_id)
        if session_id and type(session_id) is str:
            kwargs = {
                "user_id": user_id,
                "session_id": session_id
            }
            session = UserSession(**kwargs)
            session.save()
            return session_id
    
    def user_id_for_session_id(self, session_id=None):
        """ user id for session db """
        session = UserSession.search({"session_id": session_id})
        if session is None:
            return None
        current_time = datetime.now()
        elapsed_time = timedelta(seconds=self.session_duration)
        if session[0].created_at + elapsed_time < current_time:
            return None
        return session[0].user_id

    def destroy_session(self, request=None):
        """ destroy session method """
        session_id = self.session_cookie(request)
        session = UserSession.search({"session_id": session_id})
        if session is None:
            return False
        session[0].remove()
        return True
