import pytest

from datacontest.app import create_app
from datacontest.settings import TestConfig


@pytest.yield_fixture(scope='function')
def app():
    return create_app(TestConfig)
