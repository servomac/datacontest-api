from datacontest.use_cases import request_objects as ro


def test_build_datathon_list_request_object_without_parameters():
    req = ro.DatathonListRequestObject()

    assert req.filters is None
    assert bool(req) is True


def test_build_datathon_list_request_object_from_empty_dict():
    req = ro.DatathonListRequestObject.from_dict({})

    assert req.filters is None
    assert bool(req) is True


def test_build_datathon_list_request_object_with_empty_filters():
    req = ro.DatathonListRequestObject(filters={})

    assert req.filters == {}
    assert bool(req) is True


def test_build_datathon_list_request_object_from_dict_with_empty_filters():
    req = ro.DatathonListRequestObject.from_dict({'filters': {}})

    assert req.filters == {}
    assert bool(req) is True


def test_build_datathon_list_request_object_with_filters():
    req = ro.DatathonListRequestObject(filters={'a': 1, 'b': 2})

    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_datathon_list_request_object_from_dict_with_filters():
    req = ro.DatathonListRequestObject.from_dict({'filters': {'a': 1, 'b': 2}})

    assert req.filters == {'a': 1, 'b': 2}
    assert bool(req) is True


def test_build_datathon_list_request_object_from_dict_with_invalid_filters():
    req = ro.DatathonListRequestObject.from_dict({'filters': 5})

    assert req.has_errors()
    assert req.errors[0]['parameter'] == 'filters'
    assert bool(req) is False
