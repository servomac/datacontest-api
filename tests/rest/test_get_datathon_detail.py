import datetime
import json
from unittest import mock

from datacontest.domain.models import Datathon
from datacontest.shared import response_object as res

datathon = {
    'id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
    'title': 'Datathon1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
    'end_date': datetime.datetime(2018, 1, 5, 18, 20, 9, 910076)
}


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonDetailUseCase')
def test_get(mock_use_case, client):
    use_case_response_success = res.ResponseSuccess(
        Datathon.from_dict(datathon)
    )
    mock_use_case().execute.return_value = use_case_response_success

    response = client.get('/datathons/{}'.format(datathon['id']))

    expected_datathon = datathon
    expected_datathon['end_date'] = expected_datathon['end_date'].isoformat()

    assert json.loads(response.data.decode('utf-8')) == expected_datathon
    assert response.status_code == 200
    assert response.mimetype == 'application/json'


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonDetailUseCase')
def test_get_not_found(mock_use_case, client):
    response_failure = res.ResponseFailure.build_resource_error('Id not found')
    mock_use_case().execute.return_value = response_failure

    response = client.get('/datathons/any_id')

    assert response.status_code == 404
    assert response.mimetype == 'application/json'
    assert json.loads(response.data.decode('utf-8')) == {
        'message': 'Id not found',
        'type': 'ResourceError',
    }
