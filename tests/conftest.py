import os
import pytest

from app.app import app as flask_app


@pytest.fixture
def app():
    os.environ['TOKEN'] = 'my-token'
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def valid_token():
    return 'my-token'
