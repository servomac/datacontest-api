import datetime
import pytest
from unittest import mock

from datacontest.domain import models
from datacontest.repositories.user import memrepo


user_1 = {
    'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
    'username': 'user1',
    'password': 'pass',
    'email': '1@email.com',
    'created_at': datetime.datetime(2018, 1, 4, 20, 15, 0, 0),
    'is_admin': False,
}

user_2 = {
    'id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    'username': 'user2',
    'password': 'pass',
    'email': '2@email.com',
    'created_at': datetime.datetime(2018, 1, 5, 20, 0, 0, 0),
    'is_admin': False,
}


@pytest.fixture
def users():
    return [user_1, user_2]


def test_user_memrepo_list_without_parameters(users):
    repo = memrepo.UserMemRepo(users)
    assert repo.list() == users


@mock.patch('bcrypt.hashpw')
def test_repository_list_add(mocked_hashpw, users):
    mocked_hashpw.return_value = 'mocked'

    repo = memrepo.UserMemRepo(users)

    user_3 = {
        'id': 'g23236a4-5085-41e9-86dc-29d6923010s6',
        'username': 'user3',
        'password': 'pass',
        'email': '3@email.com'
    }
    created_user = repo.add(**user_3)

    assert isinstance(created_user, models.User)
    assert len(repo.list()) == 3

    by_email = repo.list(filters={'email': '3@email.com'})
    assert len(by_email) == 1
    assert by_email[0].id == 'g23236a4-5085-41e9-86dc-29d6923010s6'
    assert by_email[0].hash == 'mocked'
