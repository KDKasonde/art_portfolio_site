import pytest
from flask import session, current_app, json
from mdurocherart.login_manager import (
    LoginManager,
    login_user,
    login_required,
    _create_identifier,
    _get_remote_addr
)
USERNAME = 'tester'
PASSWORD = 'testing'


def test_verification(app):
    with app.app_context():
        status = current_app.login_manager.verify(
            username=USERNAME,
            password=PASSWORD.encode('utf-8')
        )

    assert status is True


def test_verification_wrong_password(app):
    with app.app_context():
        status = current_app.login_manager.verify(
            username=USERNAME,
            password="asdasd".encode('utf-8')
        )

    assert status is False


def test_verification_wrong_username(app):
    with app.app_context():
        status = current_app.login_manager.verify(
            username="OASJdksjnfiu0",
            password=PASSWORD.encode('utf-8')
        )

    assert status is False


def test_verify_session(client):
    with client:
        client.post(
            "/test/login",
            data={
                "current-username": USERNAME,
                "current-password": PASSWORD
            }
        )

        status = client.get(
            "/test/loggedin"
        )
        assert status.status_code == 200


def test_verify_session_no_session(client):
    with client:
        status = client.get(
            "/test/loggedin",
            headers={
                "User-Agent": "tester_net/1.0"
            }
        )
        assert status.status_code != 200
        assert status.status_code == 302


def test_verify_session_hijacked_session(client):
    with client:
        client.post(
            "/test/login",
            data={
                "current-username": USERNAME,
                "current-password": PASSWORD
            },
            headers={
                "User-Agent": "tester_net/1.0"
            }
        )

        sess = {key: value for (key, value) in session.items()}
        status = client.get(
            "/test/loggedin",
            headers={
                "Cookie": f'"{sess["_id"]}={sess["_id"]}"; '
            }
        )

        assert status.status_code != 200
        assert status.status_code == 302
