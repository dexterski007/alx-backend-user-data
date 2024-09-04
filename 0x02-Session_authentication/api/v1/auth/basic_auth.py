#!/usr/bin/env python3
"""
basic auth module for the API
"""
from api.v1.auth.auth import Auth
from flask import Flask, request
from typing import List, TypeVar, Tuple
from models.user import User
import base64
import binascii
import re


class BasicAuth(Auth):
    """ Class for basic Auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 header """
        if authorization_header is None:
            return None
        if not type(authorization_header) is str:
            return None
        if authorization_header[0:6] == "Basic ":
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Base64 Decoder method """
        if base64_authorization_header is None:
            return None
        if not type(base64_authorization_header) is str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header,
                                       validate=True)
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """ Method for user creds extraction """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not type(decoded_base64_authorization_header) is str:
            return (None, None)
        pattern = r'((?P<user>[^:]+):(?P<pass>.+))'
        match = re.fullmatch(pattern,
                             decoded_base64_authorization_header.strip())
        if match is not None:
            user = match.group('user')
            passw = match.group('pass')
            return (user, passw)
        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Method for user object from creds """
        if user_email is None or not type(user_email) is str:
            return None
        if user_pwd is None or not type(user_pwd) is str:
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) == 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method for current user """
        auth_head = self.authorization_header(request)
        base64_head = self.extract_base64_authorization_header(auth_head)
        decoded = self.decode_base64_authorization_header(base64_head)
        mail, pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(mail, pwd)
