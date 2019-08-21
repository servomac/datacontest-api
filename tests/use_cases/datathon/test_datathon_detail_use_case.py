import datetime
from unittest import mock

from datacontest.domain import models
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import datathon_use_cases as uc


def test_datathon_detail_success():
    datathon = models.Datathon(
        '91090b75-65e9-4253-975c-6f8ad0eaa955',
        title='Title1',
        subtitle='Subtitle1',
        description='Description1',
        metric='AUC',
        start_date=datetime.datetime(2018, 1, 6, 10, 15, 0, 0),
        end_date=datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
        organizer_id='971ce791-489b-46ab-ae78-a5eca3beaa5a',
    )

    repo = mock.Mock()
    repo.find_by_id.return_value = datathon

    datathon_detail_use_case = uc.DatathonDetailUseCase(repo)
    request_object = req.DatathonDetailRequestObject.from_dict({'id': 'uuid'})

    response_object = datathon_detail_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.find_by_id.assert_called_with('uuid')

    assert response_object.value == datathon


def test_datathon_detail_not_found():
    repo = mock.Mock()
    repo.find_by_id.return_value = None

    datathon_detail_use_case = uc.DatathonDetailUseCase(repo)
    request_object = req.DatathonDetailRequestObject('uuid')

    response_object = datathon_detail_use_case.execute(request_object)

    assert bool(response_object) is False
    repo.find_by_id.assert_called_with('uuid')

    assert response_object.value == {
        'message': 'Id not found',
        'type': 'ResourceError'
    }
