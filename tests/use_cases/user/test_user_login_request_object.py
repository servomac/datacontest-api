import pytest
from datacontest.use_cases import request_objects as ro


def test_build_user_login_request_object_without_params():
    with pytest.raises(TypeError):
        ro.UserLoginRequestObject()


def test_build_user_login_request_object_from_empty_dict():
    req = ro.UserLoginRequestObject.from_dict({})

    assert bool(req) is False
    assert req.has_errors()

    msg = 'Its a mandatory parameter!'
    assert req.errors == [
        {'parameter': 'username', 'message': msg},
        {'parameter': 'password', 'message': msg},
    ]


def test_build_user_login_request_object_from_dict_with_non_string_input():
    req = ro.UserLoginRequestObject.from_dict({
        'username': [],
        'password': False,
    })

    assert bool(req) is False
    assert req.has_errors()

    assert req.errors == [
        {'parameter': 'username', 'message': 'Must be a string.'},
        {'parameter': 'password', 'message': 'Must be a string.'},
    ]


def test_build_user_login_request_object_from_valid_dict():
    req = ro.UserLoginRequestObject.from_dict({
        'username': 'username',
        'password': 'password',
    })

    assert bool(req) is True
    assert req.username == 'username'
    assert req.password == 'password'
