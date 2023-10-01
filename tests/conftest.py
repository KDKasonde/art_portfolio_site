import os
import tempfile
import pytest
from mdurocherart import create_app
from flask_mailman import Mail
from mdurocherart.db import CouchdbConnection


@pytest.fixture
def app():

    app = create_app(env='test')
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mail_client(app):
    with app.app_context():
        yield Mail(app)


@pytest.fixture()
def couch_db_app_conn(app):
    with app.app_context():
        yield CouchdbConnection.from_flask_config(app)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()