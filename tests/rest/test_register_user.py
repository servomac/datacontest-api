import datetime
import json
from unittest import mock

from datacontest.domain.models import User
from datacontest.serializers import user_serializer
from datacontest.shared import response_object as res


@mock.patch('datacontest.use_cases.user_use_cases.UserRegistrationUseCase')
@mock.patch('bcrypt.hashpw')
def test_rest_user_registration(mocked_hashpw, mock_use_case, client, capsys):
    mocked_hashpw.return_value = 'mocked'
    new_user = User.from_dict({
        'id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
        'username': 'username',
        'password': 'password',
        'email': 'email@email.com',
        'created_at': datetime.datetime(2018, 1, 1),
        'is_admin': False,
    })
    mock_use_case().execute.return_value = res.ResponseCreationSuccess(new_user)


    body = {'username': 'u', 'password': 'p', 'email': 'e@e.e'}
    response = client.post('/user/registration', data=json.dumps(body), mimetype='application/json')

    print(response.data)
    serialized_user = json.dumps(new_user, cls=user_serializer.UserEncoder)
    assert response.data.decode('utf-8') == serialized_user
    assert response.status_code == 201
    assert response.mimetype == 'application/json'
