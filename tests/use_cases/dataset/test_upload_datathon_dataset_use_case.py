import datetime

from unittest import mock

from freezegun import freeze_time

from datacontest.domain import models
from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import dataset_use_cases as uc


TARGET_COLUMN = 'target'
VALID_CSV = """
col1,col2,target
0,0,0
0,1,1
"""

def test_upload_datathon_dataset_without_parameters():
    datathon_repo = mock.Mock()
    dataset_repo = mock.Mock()

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({})

    response_object = use_case.execute(request_object)

    # TODO aixo no m'agrada perque estic responent a l'usuari que necessita introduir user_id quan no és vera
    # estic 'leacking' informació interna de paràmetres de l'API del request object, quan l'usuari final del
    # l'api rest enviarà un token, no el seu user_id... revisar!
    # idea1: domés és un problema si ho expos al usuari via rest, no esta malament que ho respongui l'use case
    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'datathon_id: Its a mandatory parameter!\n'
                   'user_id: Its a mandatory parameter!\n'
                   'training: Its a mandatory parameter!\n'
                   'validation: Its a mandatory parameter!\n'
                   'test: Its a mandatory parameter!\n'
                   'target_column: Its a mandatory parameter!',
        'type': res.ResponseFailure.PARAMETERS_ERROR,
    }


def test_upload_datathon_dataset_datathon_not_found():
    datathon_repo = mock.Mock()
    datathon_repo.find_by_id.return_value = None
    dataset_repo = mock.Mock()

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_identifier',
        'user_id': 'organizer_identifier',
        'training': VALID_CSV,
        'validation': VALID_CSV,
        'test': VALID_CSV,
        'target_column': TARGET_COLUMN,
    })

    response_object = use_case.execute(request_object)

    datathon_repo.find_by_id.assert_called_with('datathon_identifier')
    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'Datathon not found.',
        'type': res.ResponseFailure.RESOURCE_ERROR,
    }


@freeze_time('2018-01-01')
def test_upload_datathon_dataset_user_is_not_datathon_organizer():
    datathon_repo = mock.Mock()
    datathon_repo.find_by_id.return_value = models.Datathon.from_dict({
        'id': 'datathon_identifier',
        'organizer_id': 'organizer_identifier',
        'title': 'title',
        'subtitle': 'subtitle',
        'description': 'desc',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
    })
    dataset_repo = mock.Mock()

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_identifier',
        'user_id': 'not_organizer!',
        'training': VALID_CSV,
        'validation': VALID_CSV,
        'test': VALID_CSV,
        'target_column': TARGET_COLUMN,
    })

    response_object = use_case.execute(request_object)

    datathon_repo.find_by_id.assert_called_with('datathon_identifier')
    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'Only the organizer of a datathon can upload a dataset.',
        'type': res.ResponseFailure.AUTHENTICATION_ERROR,
    }


@freeze_time('2018-01-01')
def test_upload_datathon_dataset_failure():
    domain_datathon = models.Datathon.from_dict({
        'id': 'datathon_id',
        'organizer_id': 'organizer_id',
        'title': 'title',
        'subtitle': 'subtitle',
        'description': 'desc',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
    })

    datathon_repo = mock.Mock()
    datathon_repo.find_by_id.return_value = domain_datathon
    dataset_repo = mock.Mock()
    dataset_repo.add.return_value = None

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'organizer_id',
        'training': VALID_CSV,
        'validation': VALID_CSV,
        'test': VALID_CSV,
        'target_column': TARGET_COLUMN,
    })

    response_object = use_case.execute(request_object)

    assert response_object.value == {
        'type': res.ResponseFailure.RESOURCE_ERROR,
        'message': 'Error adding the dataset to the repository',
    }
    assert bool(response_object) is False


@freeze_time('2018-01-01')
def test_upload_datathon_dataset_success():
    domain_datathon = models.Datathon.from_dict({
        'id': 'datathon_id',
        'organizer_id': 'organizer_id',
        'title': 'title',
        'subtitle': 'subtitle',
        'description': 'desc',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
    })
    domain_dataset = models.Dataset.from_dict({
        'id': 'dataset_id',
        'datathon_id': 'datathon_id',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'any',
    })

    datathon_repo = mock.Mock()
    datathon_repo.find_by_id.return_value = domain_datathon
    dataset_repo = mock.Mock()
    dataset_repo.build_primary_key.return_value = 'dataset_id'
    dataset_repo.add.return_value = domain_dataset

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'organizer_id',
        'training': VALID_CSV,
        'validation': VALID_CSV,
        'test': VALID_CSV,
        'target_column': TARGET_COLUMN,
    })

    response_object = use_case.execute(request_object)

    datathon_repo.find_by_id.assert_called_once_with('datathon_id')
    dataset_repo.add.assert_called_once_with(
        id='dataset_id',
        datathon_id='datathon_id',
        training=VALID_CSV,
        validation=VALID_CSV,
        test=VALID_CSV,
        target_column=TARGET_COLUMN
    )
    assert bool(response_object) is True
    assert response_object.value == domain_dataset

# TODO als tests de user use cases he testetjat un side effect de l'add, i aquí no
# com ho faig? homogeneitzar

@freeze_time('2018-01-06')
def test_upload_datathon_dataset_after_datathon_started():
    domain_datathon = models.Datathon.from_dict({
        'id': 'datathon_id',
        'organizer_id': 'organizer_id',
        'title': 'title',
        'subtitle': 'subtitle',
        'description': 'desc',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 6, 13, 15, 0, 0),
    })
    domain_dataset = models.Dataset.from_dict({
        'id': 'dataset_id',
        'datathon_id': 'datathon_id',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'any',
    })

    datathon_repo = mock.Mock()
    datathon_repo.find_by_id.return_value = domain_datathon
    dataset_repo = mock.Mock()
    dataset_repo.build_primary_key.return_value = 'dataset_id'
    dataset_repo.add.return_value = domain_dataset

    use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({
        'datathon_id': 'datathon_id',
        'user_id': 'organizer_id',
        'training': VALID_CSV,
        'validation': VALID_CSV,
        'test': VALID_CSV,
        'target_column': TARGET_COLUMN,
    })

    response_object = use_case.execute(request_object)

    datathon_repo.find_by_id.assert_called_once_with('datathon_id')
    dataset_repo.add.assert_not_called()

    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'You can only upload a dataset before the start date.',
        'type': 'ParametersError'
    }
