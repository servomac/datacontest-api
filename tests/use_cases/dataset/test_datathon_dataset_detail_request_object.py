import pytest

from datacontest.use_cases import request_objects as ro


def test_build_datathon_dataset_detail_request_object_success():
    req = ro.DatathonDatasetDetailRequestObject(datathon_id='uuid', user_id='uuid')

    assert bool(req) is True
    assert req.datathon_id == 'uuid'
    assert req.user_id == 'uuid'


def test_build_datathon_dataset_detail_request_object_without_params():
    with pytest.raises(TypeError):
        ro.DatathonDatasetDetailRequestObject()


def test_build_datathon_dataset_detail_request_object_from_dict():
    req = ro.DatathonDatasetDetailRequestObject.from_dict({'datathon_id': 'uuid', 'user_id': 'uuid'})

    assert bool(req) is True
    assert req.datathon_id == 'uuid'
    assert req.user_id == 'uuid'


def test_build_datathon_dataset_detail_request_object_from_empty_dict():
    req = ro.DatathonDatasetDetailRequestObject.from_dict({})

    assert req.has_errors()
    assert req.errors == [{
        'parameter': 'datathon_id',
        'message': 'Its a mandatory parameter!',
    },
    {
        'parameter': 'user_id',
        'message': 'Its a mandatory parameter!',
    }]
    assert bool(req) is False


def test_build_datathon_dataset_detail_request_object_from_dict_with_invalid_id():
    req = ro.DatathonDatasetDetailRequestObject.from_dict({'datathon_id': None, 'user_id': 1})

    assert req.has_errors()
    assert req.errors == [{
        'parameter': 'datathon_id',
        'message': 'Should be a valid uuid.',
    },
    {
        'parameter': 'user_id',
        'message': 'Should be a valid uuid.',
    }]
    assert bool(req) is False
