import pytest

from datacontest.use_cases import request_objects as ro


def test_build_datathon_detail_request_object_success():
    req = ro.DatathonDetailRequestObject(id='uuid')

    assert bool(req) is True
    assert req.id == 'uuid'


def test_build_datathon_detail_request_object_without_params():
    with pytest.raises(TypeError):
        req = ro.DatathonDetailRequestObject()


def test_build_datathon_detail_request_object_from_dict():
    req = ro.DatathonDetailRequestObject.from_dict({'id': 'uuid'})

    assert bool(req) is True
    assert req.id == 'uuid'


def test_build_datathon_detail_request_object_from_empty_dict():
    req = ro.DatathonDetailRequestObject.from_dict({})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'id'
    assert bool(req) is False


def test_build_datathon_detail_request_object_from_dict_with_invalid_id():
    req = ro.DatathonDetailRequestObject.from_dict({'id': None})

    assert req.has_errors()
    assert req.errors == [{
        'parameter': 'id',
        'message': 'Should be a valid uuid.'
    }]
    assert bool(req) is False
