import datetime
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
def test_build_user_from_dict_with_required_params():
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
    assert user.password == 'password'
    assert user.email == 'email@false.com'
    assert user.created_at == datetime.datetime(2017, 12, 30)
    assert user.is_admin == False


@freeze_time('2017-12-30')
def test_build_user_from_dict_with_all_params():
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
    assert user.password == 'password'
    assert user.email == 'email@email.com'
    assert user.created_at == created_at
    assert user.is_admin == 'is_admin'


@freeze_time('2017-12-30')
def test_build_user_with_default_params():
    identifier = '54fdfd17-3004-4666-8094-ba402995fa31'
    user = models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')

    assert isinstance(user, DomainModel)
    assert isinstance(user, models.User)
    assert user.id == identifier
    assert user.username == 'username'
    assert user.password == 'password'
    assert user.email == 'email@false.com'
    assert user.created_at == datetime.datetime(2017, 12, 30)
    assert user.is_admin == False