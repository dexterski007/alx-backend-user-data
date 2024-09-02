#!/usr/bin/env python3
"""
basic auth module for the API
"""
from api.v1.auth.auth import Auth
from flask import Flask, request
from typing import List, TypeVar
import base64


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
        except:
            return None
