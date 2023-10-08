import pytest
from flask import session, current_app
from mdurocherart.login_manager import (
    LoginManager,
    login_user,
    login_required,
    _create_identifier,
    _get_remote_addr
)
USERNAME = 'tester'
PASSWORD = 'testing'


def test_login(client):
    with client:
        client.post(
            "/test/login",
            data={
                "current-username": USERNAME,
                "current-password": PASSWORD
            },
            headers={
                "User-Agent": "test/1.0"
            }
        )
        sess = session
        assert "_id" in sess.keys()
        assert "_fresh" in sess.keys()
        assert "_remember" in sess.keys()


def test_login_sessions(client):
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
        sess1_id = session['_id']

        client.post(
            "/test/login",
            data={
                "current-username": USERNAME,
                "current-password": PASSWORD
            },
            headers={
                "User-Agent": "testing_network/2.0"
            }
        )
        sess2_id = session['_id']

        current_session = current_app.login_manager.active_id
        assert sess1_id != sess2_id
        assert current_session != sess1_id
        assert current_session == sess2_id