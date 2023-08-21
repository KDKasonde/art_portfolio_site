import os
import tempfile

import pytest
from mdurocherart import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db()

    yield app

    with app.app_context():
        close_db()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()