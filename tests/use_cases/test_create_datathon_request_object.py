import datetime
import pytest

from datacontest.use_cases import request_objects as ro


def test_build_create_datathon_request_object_without_params():
    with pytest.raises(TypeError):
        ro.CreateDatathonRequestObject()


def test_build_create_datathon_request_object_from_empty_dict():
    # TODO only when passed another type of object subtitle, metric and end_date should complain about the string
    # validation for non required parameter, as well as default values, is not tested nor implemented
    req = ro.CreateDatathonRequestObject.from_dict({})

    assert bool(req) is False
    assert req.has_errors()

    mandatory_param_msg = 'Its a mandatory parameter!'
    assert req.errors == [
        {'parameter': 'organizer_id', 'message': mandatory_param_msg},
        {'parameter': 'title', 'message': mandatory_param_msg},
        {'parameter': 'description', 'message': mandatory_param_msg},
    ]


def test_build_create_datathon_request_object_schema_validation():
    # TODO i.e. valid date, valid metric, title length, organizer_id is a str..
    pass


def test_build_create_datathon_request_object_from_valid_dict():
    req = ro.CreateDatathonRequestObject.from_dict({
        'title': 'Title',
        'subtitle': 'Subtitle',
        'description': 'This is a datathon, have fun!',
        'organizer_id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
        'metric': 'AUC',
        'end_date': '2018-01-01T10:10:10',
    })

    assert bool(req) is True
    assert req.organizer_id == '971ce791-489b-46ab-ae78-a5eca3beaa5a'
    assert req.title == 'Title'
    assert req.subtitle == 'Subtitle'
    assert req.description == 'This is a datathon, have fun!'
    assert req.metric == 'AUC'
    assert req.end_date == datetime.datetime(2018, 1, 1, 10, 10, 10)


def test_build_create_datathon_request_object_with_default_values():
    req = ro.CreateDatathonRequestObject.from_dict({
        'title': 'Title',
        'description': 'This is a datathon, have fun!',
        'organizer_id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
        'end_date': '2018-01-01T10:10:10',
    })

    assert bool(req) is True
    assert req.organizer_id == '971ce791-489b-46ab-ae78-a5eca3beaa5a'
    assert req.title == 'Title'
    assert req.subtitle == ''
    assert req.description == 'This is a datathon, have fun!'
    assert req.metric == 'AUC'
    assert req.end_date == datetime.datetime(2018, 1, 1, 10, 10, 10)
