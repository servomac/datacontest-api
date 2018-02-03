from unittest import mock
import json


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
                           data=json.dumps({'access_token': 'blabla'}),
                           content_type='application/json')

    assert mock_jwt_identity.called
    assert json.loads(response.data) == {
        'message': 'User not found!',
        'type': 'AuthorizationError',
    }
    assert response.status_code == 401
