#!/usr/bin/env python3
"""
Main file
"""
import requests


SERVER = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """ register user module """
    response = requests.post(
        f"{SERVER}/users", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ log_in_wrong_password user module """
    response = requests.post(
        f"{SERVER}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ log_in user module """
    response = requests.post(
        f"{SERVER}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """ profile_unlogged user module """
    response = requests.get(f"{SERVER}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile_logged user module """
    response = requests.get(f"{SERVER}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ log_out user module """
    response = requests.delete(f"{SERVER}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ reset_password_token user module """
    response = requests.post(f"{SERVER}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update_password user module """
    response = requests.put(f"{SERVER}/reset_password",
                            data={"email": email, "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
