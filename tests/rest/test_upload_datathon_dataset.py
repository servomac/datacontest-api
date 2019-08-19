import datetime
import json

from unittest import mock

from freezegun import freeze_time

from datacontest.domain.models import User, Datathon


API_ENDPOINT = '/datathons/{datathon_id}/dataset'


def test_upload_datathon_dataset_unauthenticated(client):
    response = client.post(
        API_ENDPOINT.format(datathon_id='unexistent'),
        data=json.dumps({}),
        content_type='application/json'
    )

    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError'
    }
    assert response.status_code == 401


@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_upload_datathon_with_non_existent_user(mock_jwt_identity, client):
    mock_jwt_identity.return_value = None

    response = client.post(
        API_ENDPOINT.format(datathon_id='unexistent'),
        data=json.dumps({}),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'message': 'User not found!',
        'type': 'AuthorizationError',
    }
    assert response.status_code == 401


@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_upload_datathon_dataset_to_non_existent_datathon(mock_jwt_identity, client):
    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    response = client.post(
        API_ENDPOINT.format(datathon_id='unexistent'),
        data=json.dumps({
            'training': 'any',
            'validation': 'any',
            'test': 'any',
            'target_column': 'any',
        }),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json')

    assert json.loads(response.data) == {
        'message': 'Datathon not found.',
        'type': 'ResourceError'
    }
    assert response.status_code == 404


@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_upload_datathon_dataset_without_required_parameters(mock_jwt_identity, client):
    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    response = client.post(
        API_ENDPOINT.format(datathon_id='unexistent'),
        data=json.dumps({}),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json')

    # TODO ara que ho pens, la resposta hauria de ser diferent, tipus {'type': 'ParameterError', 'messages: bla bla¿?}
    # es molt raro retornar una llista..
    assert json.loads(response.data) == [
        {'message': 'Its a mandatory parameter!', 'parameter': 'training'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'validation'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'test'},
        {'message': 'Its a mandatory parameter!', 'parameter': 'target_column'},
    ]
    assert response.status_code == 400


@freeze_time('2018-01-01')
@mock.patch('datacontest.repositories.datathon.memrepo.DatathonMemRepo.find_by_id')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_upload_datathon_dataset_without_being_the_organizer(mock_jwt_identity, mock_mem_repo, client):
    mock_mem_repo.return_value = Datathon.from_dict({
        'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'title': 'Title1',
        'subtitle': 'Subtitle1',
        'description': 'Description1',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 5, 15, 15, 0, 0),
        'organizer_id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    })

    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    response = client.post(
        API_ENDPOINT.format(datathon_id='unexistent'),
        data=json.dumps({
            'training': 'any',
            'validation': 'any',
            'test': 'any',
            'target_column': 'any',
        }),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    assert json.loads(response.data) == {
        'message': 'Only the organizer of a datathon can upload a dataset.',
        'type': 'AuthenticationError',
    }
    assert response.status_code == 403


@freeze_time('2018-01-01')
@mock.patch('datacontest.repositories.dataset.memrepo.DatasetMemRepo.build_primary_key')
@mock.patch('datacontest.repositories.datathon.memrepo.DatathonMemRepo.find_by_id')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_upload_datathon_dataset(mock_jwt_identity, mock_mem_repo, mock_dataset_mem_repo, client):
    mock_dataset_mem_repo.return_value = 'new_dataset_id'
    mock_mem_repo.return_value = Datathon.from_dict({
        'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'title': 'Title1',
        'subtitle': 'Subtitle1',
        'description': 'Description1',
        'metric': 'AUC',
        'start_date': datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
        'organizer_id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    })

    authenticated_user_mock = User('f4b236a4-5085-41e9-86dc-29d6923010b3', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    response = client.post(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        data=json.dumps({
            'training': 'any',
            'validation': 'any',
            'test': 'any',
            'target_column': 'target_column',
        }),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    mock_mem_repo.assert_called_with('91090b75-65e9-4253-975c-6f8ad0eaa955')
    assert json.loads(response.data) == {
        'datathon_id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'id': 'new_dataset_id',
        'test': 'any',
        'training': 'any',
        'validation': 'any',
        'target_column': 'target_column',
    }
    assert response.status_code == 201
