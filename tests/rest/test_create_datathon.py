import json


def test_create_datathon_unauthenticated(client):
    response = client.post('/datathons',
                data=json.dumps(
                    {}
                ),
                content_type='application/json')

    assert response.status_code == 401
    assert json.loads(response.data) == {
        'message': 'No token provided.',
        'type': 'AuthorizationError'
    }
