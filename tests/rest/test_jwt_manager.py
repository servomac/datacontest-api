import datetime
import time
import pytest
import jwt
from unittest import mock

from freezegun import freeze_time

from datacontest.domain import models
from datacontest.rest.jwt import JWTManager
from datacontest.rest.jwt import JWTException
from datacontest.rest.jwt import jwt_current_identity


@pytest.fixture
@mock.patch('bcrypt.hashpw')
def domain_user(mocked_hashpw):
    mocked_hashpw.return_value = ''
    identifier = 'bf7fa690-b8a0-4e04-b668-55ac224f7019'
    return models.User(id=identifier,
                       username='username',
                       password='password',
                       email='email@false.com')


def test_build_jwt_manager_empty_params():
    jwt = JWTManager()

    assert hasattr(jwt, 'secret')
    assert jwt.identity_field == 'id'
    assert jwt.expiration_field == 'exp'


def test_build_jwt_manager_with_secret():
    default_jwt = JWTManager()
    jwt = JWTManager(secret='supersecret')

    assert jwt.secret == 'supersecret'
    assert default_jwt.secret != jwt.secret


@mock.patch('jwt.encode')
@freeze_time('2017-12-30')
def test_jwt_manager_build_token(mocked_jwt_encode):
    mocked_jwt_encode.return_value = 'mocked_encoded'.encode('utf-8')

    jwt = JWTManager()

    token = jwt.build_token('uuid', expiration_days=2)

    now = datetime.datetime.utcnow()
    mocked_jwt_encode.assert_called_with({
        jwt.identity_field: 'uuid',
        jwt.expiration_field: now + datetime.timedelta(days=2),
    }, jwt.secret)

    assert isinstance(token, str)
    assert token == 'mocked_encoded'


@freeze_time('2017-12-30')
def test_jwt_manager_build_and_decode_token():
    jwt = JWTManager()
    token = jwt.build_token('uuid', 1)

    expected_expiration = int(time.mktime(
        (datetime.datetime.utcnow() + datetime.timedelta(days=1)).timetuple()
    ))

    assert jwt.decode_token(token) == {
        jwt.identity_field: 'uuid',
        jwt.expiration_field: expected_expiration,
    }


def test_jwt_manager_decode_failure_token_invalid_secret():

    invalid_token = jwt.encode({'id': 'test'}, 'false_secret')
    with pytest.raises(JWTException) as jwt_exception:
        JWTManager().decode_token(invalid_token)

    assert str(jwt_exception.value) == 'Signature verification failed'


def test_jwt_manager_decode_failure_token_empty_payload():
    jwt_manager = JWTManager()
    invalid_token = jwt.encode({}, jwt_manager.secret)

    with pytest.raises(JWTException) as jwt_exception:
        jwt_manager.decode_token(invalid_token)

    assert str(jwt_exception.value) == 'The token should contain an identity field (id)'


def test_jwt_manager_decode_failure_token_invalid_expiration():

    jwt_manager = JWTManager()
    invalid_token = jwt.encode({'exp': 'expiration_date'}, jwt_manager.secret)

    with pytest.raises(JWTException) as jwt_exception:
        jwt_manager.decode_token(invalid_token)

    assert str(jwt_exception.value) == 'Expiration Time claim (exp) must be an integer.'


@freeze_time('2017-12-30')
def test_user_jwt_token(domain_user):
    jwt_manager = JWTManager()
    token = jwt_manager.build_token(domain_user.id)

    expected_expiration = int(time.mktime(
        (datetime.datetime.utcnow() + datetime.timedelta(days=15)).timetuple()
    ))

    assert jwt.decode(token, jwt_manager.secret) == {
        'id': domain_user.id,
        'exp': expected_expiration,
    }


@freeze_time('2018-01-01')
def test_get_jwt_current_identity_success(domain_user):
    user_repo = mock.Mock()
    user_repo.find_by_id.return_value = domain_user

    jwt_manager = JWTManager()
    token = jwt_manager.build_token(domain_user.id)

    user = jwt_current_identity(user_repo, token)
    user_repo.find_by_id.assert_called_with(domain_user.id)
    assert user == domain_user
    assert isinstance(user, models.User)


def test_get_jwt_current_identity_failure():
    user_repo = mock.Mock()
    user_repo.find_by_id.return_value = None

    with pytest.raises(JWTException):
        jwt_current_identity(user_repo, None)


def test_get_jwt_current_identity_not_found(domain_user):
    user_repo = mock.Mock()
    user_repo.find_by_id.return_value = None

    jwt_manager = JWTManager()
    token = jwt_manager.build_token(domain_user.id)

    user = jwt_current_identity(user_repo, token)
    user_repo.find_by_id.assert_called_with(domain_user.id)
    assert user == None
