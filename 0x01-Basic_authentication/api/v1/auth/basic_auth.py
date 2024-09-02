#!/usr/bin/env python3
"""
basic auth module for the API
"""
from api.v1.auth.auth import Auth
from flask import Flask, request
from typing import List, TypeVar


class BasicAuth(Auth):
    """ Class for basic Auth """
    pass
