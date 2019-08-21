from datacontest.use_cases import request_objects as ro


def test_build_upload_datathon_dataset_request_object_from_empty_dict():
    req = ro.UploadDatathonDatasetRequestObject.from_dict({})

    assert req.errors == [
        {'message': 'Its a mandatory parameter!', 'parameter': 'datathon_id'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'user_id'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'training'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'validation'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'test'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'target_column'},
    ]
    assert bool(req) is False


def test_build_upload_datathon_dataset_request_object_str_validation_from_dict():
    req = ro.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 1,
        'training': {},
        'test': 1,
    })

    assert req.errors == [
        {'message': 'Must be a string.', 'parameter': 'user_id'},
        {'message': 'Must be a string.', 'parameter': 'training'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'validation'},
        {'message': 'Must be a string.', 'parameter': 'test'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'target_column'},
    ]
    assert bool(req) is False


def test_build_upload_datathon_dataset_request_object_from_dict():
    req = ro.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'user_id',
        'training': 'training',
        'validation': 'validation',
        'test': 'test',
        'target_column': 'target_column',
    })

    assert bool(req) is True

