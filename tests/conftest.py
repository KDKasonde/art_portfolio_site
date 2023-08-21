import os
import tempfile
import pytest
from mdurocherart import create_app
from flask_mailman import Mail


@pytest.fixture
def app():

    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mail_client(app):
    yield Mail(app)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()