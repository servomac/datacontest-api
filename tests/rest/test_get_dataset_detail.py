import datetime
import json

from unittest import mock

from datacontest.domain.models import User, Datathon, Dataset
from datacontest.shared import response_object as res


API_ENDPOINT = '/datathons/{datathon_id}/dataset'


@mock.patch('datacontest.use_cases.dataset_use_cases.DatasetDetailUseCase')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_as_organizer_before_start_date(mock_jwt_identity, mock_use_case, client):
    use_case_response_success = res.ResponseSuccess([Dataset.from_dict({
        'id': 'dataset_id',
        'datathon_id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'target_column',
    })])
    mock_use_case().execute.return_value = use_case_response_success

    organizer_mock = User('f4b236a4-5085-41e9-86dc-29d6923010b3', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = organizer_mock

    response = client.get(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    assert json.loads(response.data) == [{
        'datathon_id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'id': 'dataset_id',
        'test': 'any',
        'training': 'any',
        'validation': 'any',
        'target_column': 'target_column',
    }]
    assert response.status_code == 200


@mock.patch('datacontest.use_cases.dataset_use_cases.DatasetDetailUseCase')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_get_dataset_as_non_organizer_before_start_date(mock_jwt_identity, mock_use_case, client):
    mock_use_case().execute.return_value = res.ResponseFailure.build_resource_error(
        'Datathon has not started yet!'
    )

    non_organizer_mock = User('uuid', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = non_organizer_mock

    response = client.get(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    assert json.loads(response.data) == {
        'message': 'Datathon has not started yet!',
        'type': 'ResourceError'
    }
    assert response.status_code == 404


def test_dataset_detail_unauthenticated_user(client):
    response = client.get(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        content_type='application/json'
    )

    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError',
    }
    assert response.status_code == 401


@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_dataset_detail_unexistent_datathon(mock_jwt_identity, client):
    user_mock = User('f4b236a4-5085-41e9-86dc-29d6923010b3', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = user_mock

    response = client.get(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    assert json.loads(response.data) == {
        'message': 'Datathon not found.',
        'type': 'ResourceError',
    }
    assert response.status_code == 404

