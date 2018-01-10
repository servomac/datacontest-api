import pytest
from datacontest.use_cases import request_objects as ro


def test_build_user_registration_request_object_without_params():
    with pytest.raises(TypeError):
        ro.UserRegistrationRequestObject()


def test_build_user_registration_request_object_from_empty_dict():
    req = ro.UserRegistrationRequestObject.from_dict({})

    assert bool(req) is False
    assert req.has_errors()

    msg = 'Its a mandatory parameter!'
    assert req.errors == [
        {'parameter':'username', 'message': msg},
        {'parameter':'password', 'message': msg},
        {'parameter':'email', 'message': msg},
    ]


def test_build_user_registration_request_object_from_dict_with_non_string_input():
    req = ro.UserRegistrationRequestObject.from_dict({
        'username': [],
        'password': None,
        'email': {},
    })

    assert bool(req) is False
    assert req.has_errors()

    assert req.errors == [
        {'parameter':'username', 'message': 'Must be a string.'},
        {'parameter':'password', 'message': 'Must be a string.'},
        {'parameter':'email', 'message': 'Must be a string.'},
    ]

def test_build_user_registration_request_object_from_dict():
    req = ro.UserRegistrationRequestObject.from_dict({
        'username': 'username',
        'password': 'password',
        'email': 'email@paco.com'
    })

    assert bool(req) is True
    assert req.username == 'username'
    assert req.password == 'password'
    assert req.email == 'email@paco.com'
