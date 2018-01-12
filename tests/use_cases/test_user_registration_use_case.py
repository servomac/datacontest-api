import datetime
from unittest import mock

import pytest

from datacontest.domain import models
from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import user_use_cases as uc


@pytest.fixture
def domain_users():
    user_1 = models.User(
        '',
        username='user1',
        password='pass1',
        email='1@email.com',
        is_admin=False,
        created_at=datetime.datetime(2018, 1, 1, 12, 15, 0, 0))

    user_2 = models.User(
        '',
        username='user2',
        password='pass2',
        email='2@email.com',
        is_admin=False,
        created_at=datetime.datetime(2018, 1, 1, 12, 15, 0, 0))

    return [user_1, user_2]


def test_user_registration_without_parameters(domain_users):
    repo = mock.Mock()

    user_registration_use_case = uc.UserRegistrationUseCase(repo)
    request_object = req.UserRegistrationRequestObject.from_dict({})

    response_object = user_registration_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'username: Its a mandatory parameter!\n'
                   'password: Its a mandatory parameter!\n'
                   'email: Its a mandatory parameter!',
        'type': 'ParametersError'
    }


def test_user_registration_without_email(domain_users):
    repo = mock.Mock()

    user_registration_use_case = uc.UserRegistrationUseCase(repo)
    request_object = req.UserRegistrationRequestObject.from_dict({
        'username': 'user',
        'password': 'pass',
    })

    response_object = user_registration_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'email: Its a mandatory parameter!',
        'type': 'ParametersError'
    }


def test_user_registration_with_existing_email(domain_users):
    repo = mock.Mock()
    repo.list.return_value = domain_users

    user_registration_use_case = uc.UserRegistrationUseCase(repo)
    request_object = req.UserRegistrationRequestObject.from_dict({
        'username': 'user',
        'password': 'pass',
        'email': '1@email.com',
    })

    response_object = user_registration_use_case.execute(request_object)

    assert bool(response_object) is False
    repo.list.assert_called_with(filters={'email': '1@email.com'})
    assert response_object.value == {
        'message': 'This email is already in use',
        'type': 'AuthenticationError',
    }


def test_user_registration_success(domain_users):
    repo = mock.Mock()
    repo.build_primary_key.return_value = 'mocked_id'
    repo.list.return_value = []
    repo.add.return_value = {
        'mock': 'response'
    }

    user_registration_use_case = uc.UserRegistrationUseCase(repo)
    request_object = req.UserRegistrationRequestObject.from_dict({
        'username': 'user',
        'password': 'pass',
        'email': 'new@email.com',
    })

    response_object = user_registration_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters={'email': 'new@email.com'})
    repo.add.assert_called_with(
        id='mocked_id',
        username='user',
        password='pass',
        email='new@email.com',
    )

    assert response_object.value == {'mock': 'response'}


def test_user_registration_handles_generic_error():
    repo = mock.Mock()
    repo.list.return_value = []
    repo.add.side_effect = Exception('Random error')

    user_registration_use_case = uc.UserRegistrationUseCase(repo)
    request_object = req.UserRegistrationRequestObject.from_dict({
        'username': 'user',
        'password': 'pass',
        'email': 'new@email.com',
    })

    response_object = user_registration_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: Random error',
    }
