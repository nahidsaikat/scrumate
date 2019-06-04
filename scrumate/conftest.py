import pytest


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass


@pytest.fixture(scope='session')
def func():
    return 1
