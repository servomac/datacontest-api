import datetime
from unittest import mock

import pytest

from datacontest.domain import models
from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import datathon_use_cases as uc


@pytest.fixture
def domain_datathons():
    datathon_1 = models.Datathon(
        '91090b75-65e9-4253-975c-6f8ad0eaa955',
        title='Title1',
        subtitle='Subtitle1',
        description='Description1',
        metric='AUC',
        start_date=datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
        end_date=datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
        organizer_id='f4b236a4-5085-41e9-86dc-29d6923010b3')

    datathon_2 = models.Datathon(
        'f4b236a4-5085-41e9-86dc-29d6923010b3',
        title='Title2',
        subtitle='Subtitle2',
        description='Description2',
        metric='AUC',
        start_date=datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
        end_date=datetime.datetime(2018, 1, 1, 13, 15, 0, 0),
        organizer_id='f4b236a4-5085-41e9-86dc-29d6923010b3')

    return [datathon_1, datathon_2]


def test_datathon_list_without_parameters(domain_datathons):
    repo = mock.Mock()
    repo.list.return_value = domain_datathons

    datathon_list_use_case = uc.DatathonListUseCase(repo)
    request_object = req.DatathonListRequestObject.from_dict({})

    response_object = datathon_list_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=None)

    assert response_object.value == domain_datathons


def test_datathon_list_with_filters(domain_datathons):
    repo = mock.Mock()
    repo.list.return_value = domain_datathons

    datathon_list_use_case = uc.DatathonListUseCase(repo)
    query_filters = {'any': 5}
    request_object = req.DatathonListRequestObject.from_dict({
        'filters': query_filters
    })

    response_object = datathon_list_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=query_filters)
    assert response_object.value == domain_datathons


def test_datathon_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception('Random error')

    datathon_list_use_case = uc.DatathonListUseCase(repo)
    request_object = req.DatathonListRequestObject.from_dict({})

    response_object = datathon_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: Random error',
    }


def test_datathon_list_handles_bad_request():
    repo = mock.Mock()

    datathon_list_use_case = uc.DatathonListUseCase(repo)
    request_object = req.DatathonListRequestObject.from_dict({'filters': 1})

    response_object = datathon_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': 'filters: Is not iterable',
    }
