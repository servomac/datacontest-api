import datetime
import json
from unittest import mock

from datacontest.domain.models import User
from datacontest.shared import response_object as res


@mock.patch('datacontest.use_cases.user_use_cases.UserLoginUseCase')
@mock.patch('jwt.encode')
@mock.patch('bcrypt.hashpw')
def test_rest_user_login(mocked_hashpw, mock_jwt_encode, mock_use_case, client, capsys):
    mocked_hashpw.return_value = 'mocked'
    user = User.from_dict({
        'id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
        'username': 'username',
        'password': 'password',
        'email': 'email@email.com',
    })
    mock_jwt_encode.return_value = 'mocked_token'.encode('utf-8')
    mock_use_case().execute.return_value = \
        res.ResponseSuccess(user)

    body = {'username': 'u', 'password': 'p'}
    response = client.post('/user/login',
                           data=json.dumps(body),
                           mimetype='application/json')

    assert json.loads(response.data.decode('utf-8')) == {
        'access_token': 'mocked_token'
    }
    assert response.status_code == 200
    assert response.mimetype == 'application/json'


@mock.patch('datacontest.use_cases.user_use_cases.UserLoginUseCase')
def test_rest_user_login_failed_response(mock_use_case, client):
    response_failure = res.ResponseFailure.build_system_error('test message')
    mock_use_case().execute.return_value = response_failure

    user = {'username': 'u', 'password': 'p'}
    response = client.post('/user/login',
                           data=json.dumps(user),
                           mimetype='application/json')

    assert json.loads(response.data.decode('utf-8')) == {
        'type': 'SystemError',
        'message': 'test message'
    }
    assert response.status_code == 500
    assert response.mimetype == 'application/json'


@mock.patch('datacontest.use_cases.user_use_cases.UserLoginUseCase')
def test_rest_user_login_authentication_failure(mock_use_case, client):
    response_failure = res.ResponseFailure.build_authentication_error(
        'test message'
    )
    mock_use_case().execute.return_value = response_failure

    user = {'username': 'u', 'password': 'p'}
    response = client.post('/user/login',
                           data=json.dumps(user),
                           mimetype='application/json')

    assert json.loads(response.data.decode('utf-8')) == {
        'type': 'AuthenticationError',
        'message': 'test message'
    }
    assert response.status_code == 403
    assert response.mimetype == 'application/json'
