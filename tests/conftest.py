import pytest

from Web import app as flask_app  ##


@pytest.fixture
def app():
  return app
