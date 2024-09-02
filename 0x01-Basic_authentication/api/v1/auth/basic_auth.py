#!/usr/bin/env python3
"""
basic auth module for the API
"""
from api.v1.auth.auth import Auth
from flask import Flask, request
from typing import List, TypeVar, Tuple
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
        except (binascii.Error):
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
