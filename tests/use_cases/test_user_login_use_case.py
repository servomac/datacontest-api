from unittest import mock

from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import user_use_cases as uc


def test_user_login_use_case_without_parameters():
    repo = mock.Mock()

    user_login_use_case = uc.UserLoginUseCase(repo)
    request_object = req.UserLoginRequestObject.from_dict({})

    response_object = user_login_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'username: Its a mandatory parameter!\n'
                   'password: Its a mandatory parameter!',
        'type': res.ResponseFailure.PARAMETERS_ERROR,
    }


def test_user_login_use_case_unexistent_user():
    repo = mock.Mock()
    repo.list.return_value = []

    user_login_use_case = uc.UserLoginUseCase(repo)
    request_object = req.UserLoginRequestObject.from_dict({
        'username': 'unexistent',
        'password': 'pass',
    })

    response_object = user_login_use_case.execute(request_object)

    repo.list.assert_called_with(filters={'username': 'unexistent'})
    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'User not found!',
        'type': res.ResponseFailure.RESOURCE_ERROR,
    }


def test_user_login_use_case_invalid_password():
    mocked_user = mock.Mock()
    mocked_user.is_valid_password.return_value = False

    repo = mock.Mock()
    repo.list.return_value = [mocked_user]

    user_login_use_case = uc.UserLoginUseCase(repo)
    request_object = req.UserLoginRequestObject.from_dict({
        'username': 'any_user',
        'password': 'any_pass',
    })

    response_object = user_login_use_case.execute(request_object)

    repo.list.assert_called_with(filters={'username': 'any_user'})
    mocked_user.is_valid_password.assert_called_with('any_pass')

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'Invalid password!',
        'type': res.ResponseFailure.AUTHORIZATION_ERROR,
    }


def test_user_login_use_case_success():
    mocked_user = mock.Mock()
    mocked_user.is_valid_password.return_value = True
    mocked_user.token = 'mocked_token'

    repo = mock.Mock()
    repo.list.return_value = [mocked_user]

    user_login_use_case = uc.UserLoginUseCase(repo)
    request_object = req.UserLoginRequestObject.from_dict({
        'username': 'any_user',
        'password': 'any_pass',
    })

    response_object = user_login_use_case.execute(request_object)

    repo.list.assert_called_with(filters={'username': 'any_user'})
    mocked_user.is_valid_password.assert_called_with('any_pass')

    assert bool(response_object) is True
    assert response_object.value == {
        'access_token': 'mocked_token'
    }
