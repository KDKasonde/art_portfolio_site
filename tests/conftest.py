import os
import tempfile
import pytest
from mdurocherart import create_app
from flask_mailman import Mail


@pytest.fixture
def app():

<<<<<<< HEAD
    app = create_app(env='test')
=======
    app = create_app()
>>>>>>> 2a397a7 (feat: add toml file along with the flask-mailman package, set up poetry env and ensure the package is stable.)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mail_client(app):
<<<<<<< HEAD
    with app.app_context():
        yield Mail(app)
=======
    yield Mail(app)
>>>>>>> 2a397a7 (feat: add toml file along with the flask-mailman package, set up poetry env and ensure the package is stable.)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()