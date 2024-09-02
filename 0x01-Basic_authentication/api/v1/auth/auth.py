#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import Flask, request
from typing import List, TypeVar
import re


class Auth:
    """ Class for Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method for require auth """
        if path is None:
            return True
        if excluded_paths is None:
            return True
        for element in map(lambda x: x.strip(), excluded_paths):
            pattern = ''
            if element[-1] == '*':
                pattern = '{}.*'.format(element[0:-1])
            elif element[-1] == '/':
                pattern = '{}/*'.format(element[0:-1])
            else:
                pattern = '{}/*'.format(element)
            if re.match(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ public method for auth header """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User public method """
        return None
