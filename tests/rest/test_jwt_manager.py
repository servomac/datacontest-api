import datetime
import time
from unittest import mock

from freezegun import freeze_time

from datacontest.rest.jwt import JWTManager


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

    mocked_jwt_encode.assert_called_with({
        jwt.identity_field: 'uuid',
        jwt.expiration_field: datetime.datetime.utcnow() + datetime.timedelta(days=2),
    }, jwt.secret)

    assert isinstance(token, str)
    assert token == 'mocked_encoded'


@freeze_time('2017-12-30')
def test_jwt_manager_build_and_decode_token():
    jwt = JWTManager()
    token = jwt.build_token('uuid', 1)

    # TODO why this hour timelapse? timezones?
    expected_expiration = 3600 + int(time.mktime(
        (datetime.datetime.utcnow() + datetime.timedelta(days=1)).timetuple()
    ))

    assert jwt.decode_token(token) == {
        jwt.identity_field: 'uuid',
        jwt.expiration_field: expected_expiration,
    }



# @freeze_time('2017-12-30')
# @mock.patch('bcrypt.hashpw')
# def test_user_jwt_token(mocked_hashpw):
#     mocked_hashpw.return_value = 'mocked_hash'

#     identifier = 'bf7fa690-b8a0-4e04-b668-55ac224f7019'
#     user = models.User(id=identifier,
#                        username='username',
#                        password='password',
#                        email='email@false.com')

#     token = user.token
#     assert isinstance(token, str)

#     import jwt
#     # TODO why this hour timelapse? timezones?
#     expected_expiration = 3600 + int(time.mktime(
#         (datetime.datetime.utcnow() + datetime.timedelta(days=15)).timetuple()
#     ))
#     # TODO where there is the logic of JWT tokens? REST layer or user domain??
#     # TODO  secret where is stored?
#     assert jwt.decode(token, user.jwt_secret) == {
#         'user_id': identifier,
#         'exp': expected_expiration,
#     }
