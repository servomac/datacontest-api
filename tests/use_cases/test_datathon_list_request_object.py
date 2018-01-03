from datacontest.use_cases import request_objects as ro


def test_build_datathon_list_request_object_without_parameters():
    req = ro.DatathonListRequestObject()

    assert bool(req) is True


def test_build_datathon_list_request_object_from_empty_dict():
    req = ro.DatathonListRequestObject.from_dict({})

    assert bool(req) is True
