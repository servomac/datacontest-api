from unittest import mock
import json


from datacontest.domain.models import User

# TODO what happens when data=None and content_type = json

def test_create_datathon_unauthenticated(client):
    response = client.post('/datathons',
                           data=json.dumps({}),
                           content_type='application/json')

    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError'
    }
    assert response.status_code == 401


@mock.patch('datacontest.rest.datathon.jwt_current_identity')
def test_create_datathon_with_non_existent_user(mock_jwt_identity, client):
    mock_jwt_identity.return_value = None

    response = client.post('/datathons',
                           data=json.dumps({'access_token': 'any'}),
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'message': 'User not found!',
        'type': 'AuthorizationError',
    }
    assert response.status_code == 401


@mock.patch('datacontest.repositories.memrepo.MemRepo.build_primary_key')
@mock.patch('datacontest.rest.datathon.jwt_current_identity')
def test_create_datathon(mock_jwt_identity, mock_mem_repo, client):
    mocked_datathon_id = 'fb3390ee-9a8e-42e9-9f81-c626bc38ba7f'
    mock_mem_repo.return_value = mocked_datathon_id

    authenticated_user_mock = User('uuid-identifier', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = authenticated_user_mock

    data = {
        'title': 'A successful datathon',
        'subtitle': 'Subtitle',
        'description': 'Lets go',
        'metric': 'AUC',
        'end_date': '2019-01-01T00:00:00',
    }
    response = client.post('/datathons',
                           data=json.dumps({**{'access_token': 'any'}, **data}),
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'id': mocked_datathon_id,
        'title': 'A successful datathon',
        'subtitle': 'Subtitle',
        'description': 'Lets go',
        'end_date': '2019-01-01T00:00:00',
        'metric': 'AUC',
        'organizer_id': 'uuid-identifier',
    }
    assert response.status_code == 201
