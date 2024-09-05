#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from typing import Tuple
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST session login
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(getattr(users[0], "id"))
    sess = os.getenv("SESSION_NAME")
    out = jsonify(users[0].to_json())
    out.set_cookie(sess, session_id)
    return out

@app_views.route('/auth_session/logout', methods=['DELETE'],
                strict_slashes=False)
def logout_session() -> Tuple[str, int]:
    """ method for logout session """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
