import datetime
from unittest import mock

import pytest
from freezegun import freeze_time

from datacontest.domain import models
from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import dataset_use_cases as uc


def test_datathon_dataset_detail_without_parameters():
    datathon_repo = mock.Mock()
    dataset_repo = mock.Mock()

    use_case = uc.DatasetDetailUseCase(datathon_repo, dataset_repo)
    request_object = req.DatathonDatasetDetailRequestObject.from_dict({})

    response_object = use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'datathon_id: Its a mandatory parameter!\n'
                   'user_id: Its a mandatory parameter!',
        'type': res.ResponseFailure.PARAMETERS_ERROR,
    }


@pytest.fixture()
def domain_dataset():
    return models.Dataset.from_dict({
        'id': 'dataset_id',
        'datathon_id': 'datathon_id',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'target_column',
    })


@pytest.fixture()
def dataset_repo(domain_dataset):
    dataset_repo = mock.Mock()
    dataset_repo.find_by.return_value = [domain_dataset]
    return dataset_repo


datathon_repo = mock.Mock()
datathon_repo.find_by_id.return_value = models.Datathon.from_dict({
    'id': 'datathon_id',
    'title': 'Title1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
    'start_date': datetime.datetime(2018, 1, 5, 0, 0, 0, 0),
    'end_date': datetime.datetime(2018, 1, 10, 0, 0, 0, 0),
    'organizer_id': 'organizer_id',
})


@freeze_time('2018-01-01')
def test_as_organizer_before_start_date(domain_dataset, dataset_repo):
    use_case = uc.DatasetDetailUseCase(datathon_repo, dataset_repo)
    request_object = req.DatathonDatasetDetailRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'organizer_id',
    })

    response_object = use_case.execute(request_object)

    assert response_object.value == [domain_dataset]
    assert bool(response_object) is True


@freeze_time('2018-01-15')
def test_as_non_organizer_when_datathon_has_ended(domain_dataset, dataset_repo):
    use_case = uc.DatasetDetailUseCase(datathon_repo, dataset_repo)
    request_object = req.DatathonDatasetDetailRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'any_user_id',
    })

    response_object = use_case.execute(request_object)

    assert response_object.value == [domain_dataset]
    assert bool(response_object) is True


@freeze_time('2018-01-06')
def test_as_non_organizer_while_datathon_is_running(dataset_repo):
    use_case = uc.DatasetDetailUseCase(datathon_repo, dataset_repo)
    request_object = req.DatathonDatasetDetailRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'any_user_id',
    })

    response_object = use_case.execute(request_object)

    assert [dataset.as_dict() for dataset in response_object.value] == [{
        'id': 'dataset_id',
        'datathon_id': 'datathon_id',
        'training': 'any',
        'validation': 'any',
        'test': 'Hidden',
        'target_column': 'target_column',
    }]
    assert bool(response_object) is True


@freeze_time('2018-01-06')
def test_as_organizer_while_datathon_is_running(dataset_repo):
    use_case = uc.DatasetDetailUseCase(datathon_repo, dataset_repo)
    request_object = req.DatathonDatasetDetailRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'organizer_id',
    })

    response_object = use_case.execute(request_object)

    assert [dataset.as_dict() for dataset in response_object.value] == [{
        'id': 'dataset_id',
        'datathon_id': 'datathon_id',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'target_column',
    }]
    assert bool(response_object) is True


def test_unexistent_datathon():
    empty_datathon_repo = mock.Mock()
    empty_datathon_repo.find_by_id.return_value = None

    use_case = uc.DatasetDetailUseCase(empty_datathon_repo, dataset_repo)

    request_object = req.DatathonDatasetDetailRequestObject.from_dict({
        'datathon_id': 'false_unexistent',
        'user_id': 'any_user_id',
    })

    response_object = use_case.execute(request_object)

    assert response_object.value == {
        'message': 'Datathon not found.',
        'type': 'ResourceError',
    }
    assert bool(response_object) is False
