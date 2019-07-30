import datetime
import pytest
from unittest import mock

from freezegun import freeze_time

from datacontest.domain import models
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
        end_date=datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
        organizer_id='f4b236a4-5085-41e9-86dc-29d6923010b3')

    datathon_2 = models.Datathon(
        'f4b236a4-5085-41e9-86dc-29d6923010b3',
        title='Title2',
        subtitle='Subtitle2',
        description='Description2',
        metric='AUC',
        end_date=datetime.datetime(2018, 1, 1, 13, 15, 0, 0),
        organizer_id='f4b236a4-5085-41e9-86dc-29d6923010b3')

    return [datathon_1, datathon_2]


def test_create_datathon_without_parameters():
    repo = mock.Mock()

    create_datathon_use_case = uc.CreateDatathonUseCase(repo)
    request_object = req.CreateDatathonRequestObject.from_dict({})

    response_object = create_datathon_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'organizer_id: Its a mandatory parameter!\n'
                   'title: Its a mandatory parameter!\n'
                   'description: Its a mandatory parameter!',
        'type': 'ParametersError',
    }


@freeze_time('2018-01-01')
def test_create_datathon_success(domain_datathons):
    repo = mock.Mock()
    repo.build_primary_key.return_value = 'mocked_id'
    repo.add.return_value = {
        'mock': 'response',
    }

    create_datathon_use_case = uc.CreateDatathonUseCase(repo)
    request_object = req.CreateDatathonRequestObject.from_dict({
        'title': 'Title',
        'subtitle': 'Subtitle',
        'description': 'Description',
        'metric': 'AUC',
        'end_date': '2018-01-01T10:10:10',
        'organizer_id': 'organizer_id',
    })

    response_object = create_datathon_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.add.assert_called_with(
        id='mocked_id',
        title='Title',
        subtitle='Subtitle',
        description='Description',
        end_date=datetime.datetime(2018,1,1,10,10,10),
        metric='AUC',
        organizer_id='organizer_id',
    )

    assert response_object.value == {'mock': 'response'}


def test_create_datathon_failure(domain_datathons):
    pass
    #repo = mock.Mock()
    #repo.add.raises ??
