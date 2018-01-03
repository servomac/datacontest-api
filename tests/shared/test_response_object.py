import pytest

from datacontest.shared import response_object as res
from datacontest.shared import request_object as req


@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_msg():
    return 'This is a response error'


def test_response_success_is_true(response_value):
    assert bool(res.ResponseSuccess(response_value)) is True


def test_response_failure_is_false(response_type, response_value):
    assert bool(res.ResponseFailure(response_type, response_value)) is False


def test_response_success_contains_value(response_value):
    response = res.ResponseSuccess(response_value)

    assert response.value == response_value


def test_response_failure_has_type_and_message(response_type, response_msg):
    response = res.ResponseFailure(response_type, response_msg)

    assert response.type == response_type
    assert response.message == response_msg


def test_response_failure_contains_value(response_type, response_msg):
    response = res.ResponseFailure(response_type, response_msg)

    assert response.value == {
        'type': response_type,
        'message': response_msg
    }


def test_response_failure_initialization_with_exception():
    response = res.ResponseFailure(response_type, Exception('Error msg'))

    assert bool(response) is False
    assert response.type == response_type
    assert response.message == "Exception: Error msg"


def test_response_failure_from_invalid_request_object():
    response = res.ResponseFailure.build_from_invalid_request_object(
        req.InvalidRequestObject()
    )

    assert bool(response) is False


def test_response_failure_from_invalid_request_object_with_errors():
    request_object = req.InvalidRequestObject()
    request_object.add_error('path', 'Is mandatory')
    request_object.add_error('path', "can't be blank")

    response = res.ResponseFailure.build_from_invalid_request_object(
        request_object
    )

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: can't be blank"


def test_response_failure_build_resource_error():
    response = res.ResponseFailure.build_resource_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.RESOURCE_ERROR
    assert response.message == "test message"


def test_response_failure_build_parameters_error():
    response = res.ResponseFailure.build_parameters_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "test message"


def test_response_failure_build_system_error():
    response = res.ResponseFailure.build_system_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.message == "test message"
