import os
import tempfile
import pytest
from mdurocherart import create_app
from flask_mailman import Mail


@pytest.fixture
def app():

<<<<<<< HEAD
<<<<<<< HEAD
    app = create_app(env='test')
=======
    app = create_app()
>>>>>>> 2a397a7 (feat: add toml file along with the flask-mailman package, set up poetry env and ensure the package is stable.)
=======
    app = create_app(env='test')
>>>>>>> 83ffea9 (add tests for emails being sent and simple fake smt server code remove hard, small edits such as coded email addr set up configs for full end to end testing)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mail_client(app):
    with app.app_context():
        yield Mail(app)

@pytest.fixture
def runner(app):
    return app.test_cli_runner()