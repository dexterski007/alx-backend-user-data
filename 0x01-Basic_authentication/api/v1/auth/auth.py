#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """ Class for Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method for require auth """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for element in excluded_paths:
            if path.rstrip('/') in element.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ public method for auth header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User public method """
        return None
