from unittest import mock
import json

from freezegun import freeze_time

from datacontest.domain.models import User


def test_create_datathon_without_json_content_type(client):
    response = client.post('/datathons', data='Hello')
    assert json.loads(response.data) == {
        'message': 'Request body must be JSON.',
        'type': 'ParametersError'
    }
    assert response.status_code == 400

    response = client.post('/datathons')
    assert json.loads(response.data) == {
        'message': 'Request body must be JSON.',
        'type': 'ParametersError'
    }
    assert response.status_code == 400


def test_create_datathon_empty_request(client):
    response = client.post('/datathons', content_type='application/json')

    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError'
    }
    assert response.status_code == 401


def test_create_datathon_unauthenticated(client):
    response = client.post('/datathons',
                           data=json.dumps({}),
                           content_type='application/json')

    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError'
    }
    assert response.status_code == 401


@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_create_datathon_with_non_existent_user(mock_jwt_identity, client):
    mock_jwt_identity.return_value = None

    response = client.post('/datathons',
                           data=json.dumps({}),
                           headers={'Authorization': 'Bearer any'},
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'message': 'User not found!',
        'type': 'AuthorizationError',
    }
    assert response.status_code == 401


@freeze_time('2018-01-01')
@mock.patch('datacontest.repositories.memrepo.MemRepo.build_primary_key')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_create_datathon_success(mock_jwt_identity, mock_mem_repo, client):
    mocked_datathon_id = 'fb3390ee-9a8e-42e9-9f81-c626bc38ba7f'
    mock_mem_repo.return_value = mocked_datathon_id

    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    data = {
        'title': 'A successful datathon',
        'subtitle': 'Subtitle',
        'description': 'Lets go',
        'metric': 'AUC',
        'start_date': '2018-01-05T00:00:00',
        'end_date': '2019-01-01T00:00:00',
    }
    response = client.post('/datathons',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer any'},
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'id': mocked_datathon_id,
        'title': 'A successful datathon',
        'subtitle': 'Subtitle',
        'description': 'Lets go',
        'start_date': '2018-01-05T00:00:00',
        'end_date': '2019-01-01T00:00:00',
        'metric': 'AUC',
        'organizer_id': 'uuid-identifier',
    }
    assert response.status_code == 201


# TODO test end date is after start date, at least 15 minutes?

@freeze_time('2019-01-01')
@mock.patch('datacontest.repositories.memrepo.MemRepo.build_primary_key')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_create_datathon_past_start_date(mock_jwt_identity, mock_mem_repo, client):
    mocked_datathon_id = 'fb3390ee-9a8e-42e9-9f81-c626bc38ba7f'
    mock_mem_repo.return_value = mocked_datathon_id

    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    data = {
        'title': 'A successful datathon',
        'subtitle': 'Subtitle',
        'description': 'Lets go',
        'metric': 'AUC',
        'start_date': '2018-01-01T00:00:00',
        'end_date': '2019-02-01T00:00:00',
    }
    response = client.post('/datathons',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer any'},
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'message': 'Start date must be in the future.',
        'type': 'ParametersError',
    }
    assert response.status_code == 400
