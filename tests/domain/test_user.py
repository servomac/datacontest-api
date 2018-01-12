import datetime
import time
import pytest
from freezegun import freeze_time
from unittest import mock

from datacontest.shared.domain_model import DomainModel
from datacontest.domain import models


def test_build_user_without_parameters():
    with pytest.raises(TypeError):
        models.User()


def test_build_user_from_empty_dict():
    with pytest.raises(KeyError):
        models.User.from_dict({})


@freeze_time('2017-12-30')
@mock.patch('bcrypt.hashpw')
def test_build_user_from_dict_with_required_params(mocked_hashpw):
    mocked_hashpw.return_value = ''

    identifier = '54fdfd17-3004-4666-8094-ba402995fa31'
    user = models.User.from_dict({
        'id': identifier,
        'username': 'username',
        'password': 'password',
        'email': 'email@false.com',
    })

    assert isinstance(user, DomainModel)
    assert isinstance(user, models.User)
    assert user.id == identifier
    assert user.username == 'username'
    assert user.email == 'email@false.com'
    assert user.created_at == datetime.datetime(2017, 12, 30)
    assert user.is_admin is False
    assert hasattr(user, 'hash')


@freeze_time('2017-12-30')
@mock.patch('bcrypt.hashpw')
def test_build_user_from_dict_with_all_params(mocked_hashpw):
    mocked_hashpw.return_value = 'mocked_hash'

    identifier = 'bf7fa690-b8a0-4e04-b668-55ac224f7019'
    created_at = datetime.datetime.now()
    user = models.User.from_dict({
        'id': identifier,
        'username': 'username',
        'password': 'password',
        'email': 'email@email.com',
        'created_at': created_at,
        'is_admin': 'is_admin'
    })

    assert user.id == identifier
    assert user.username == 'username'
    assert user.email == 'email@email.com'
    assert user.created_at == created_at
    assert user.is_admin == 'is_admin'
    assert user.hash == 'mocked_hash'


@freeze_time('2017-12-30')
@mock.patch('bcrypt.hashpw')
def test_build_user_with_default_params(mocked_hashpw):
    mocked_hashpw.return_value = 'hash'

    identifier = '54fdfd17-3004-4666-8094-ba402995fa31'
    user = models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')

    assert isinstance(user, DomainModel)
    assert isinstance(user, models.User)
    assert user.id == identifier
    assert user.username == 'username'
    assert user.email == 'email@false.com'
    assert user.created_at == datetime.datetime(2017, 12, 30)
    assert user.is_admin is False
    assert user.hash == 'hash'


def test_user_is_valid_password():
    identifier = '54fdfd17-3004-4666-8094-ba402995fa31'
    user = models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')

    assert user.is_valid_password('password') is True
    assert user.is_valid_password('any') is False


def test_user_set_password():
    identifier = '54fdfd17-3004-4666-8094-ba402995fa31'
    user = models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')

    assert user.is_valid_password('password')

    user.set_password('newpass')
    assert user.is_valid_password('newpass')


@freeze_time('2017-12-30')
@mock.patch('bcrypt.hashpw')
def test_user_jwt_token(mocked_hashpw):
    mocked_hashpw.return_value = 'mocked_hash'

    identifier = 'bf7fa690-b8a0-4e04-b668-55ac224f7019'
    user = models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')

    token = user.token
    assert isinstance(token, str)

    import jwt
    # TODO why this hour timelapse? timezones?
    expected_expiration = 3600 + int(time.mktime(
        (datetime.datetime.utcnow() + datetime.timedelta(days=15)).timetuple()
    ))
    # TODO where there is the logic of JWT tokens? REST layer or user domain??
    # TODO  secret where is stored?
    assert jwt.decode(token, 'asdjajskdhakjhasd') == {
        'user_id': identifier,
        'exp': expected_expiration,
    }
