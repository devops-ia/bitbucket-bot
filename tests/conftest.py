import os
import pytest
from unittest.mock import MagicMock

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

@pytest.fixture
def post(monkeypatch):
    """Replace requests.post so no test opens the network."""
    mock = MagicMock(return_value=MagicMock(text='ok'))
    monkeypatch.setattr('app.app.requests.post', mock)
    return mock
