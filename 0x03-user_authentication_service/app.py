#!/usr/bin/env python3
"""flask app basic
"""
from flask import Flask, jsonify, Response, request, abort
from flask import make_response, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def welcome() -> Response:
    """ main root method"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    """ route for creating users """
    email = request.form["email"]
    password = request.form["password"]
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """ route for login """
    email = request.form["email"]
    password = request.form["password"]
    answ = jsonify({"email": email, "message": "logged in"}), 200
    if AUTH.valid_login(email, password):
        resp = make_response(answ)
        resp.set_cookie('session_id', AUTH.create_session(email))
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """ route for logout """
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.user_id)
        redirect("/")
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
