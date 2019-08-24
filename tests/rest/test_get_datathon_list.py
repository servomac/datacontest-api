import datetime
import json
from unittest import mock

from datacontest.domain.models import Datathon
from datacontest.shared import response_object as res


datathon_1 = {
    'id': '971ce791-489b-46ab-ae78-a5eca3beaa5a',
    'title': 'Datathon1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
    'start_date': datetime.datetime(2018, 1, 3, 13, 15, 0, 0),
    'end_date': datetime.datetime(2018, 1, 5, 18, 20, 9, 910076),
    'organizer_id': '231c3tt1-489b-46ab-ae78-a5eca4sealfa'
}

datathons = [Datathon.from_dict(datathon_1)]


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonListUseCase')
def test_get(mock_use_case, client):
    mock_use_case().execute.return_value = res.ResponseSuccess(datathons)

    response = client.get('/datathons')

    datathon_1['start_date'] = datathon_1['start_date'].isoformat()
    datathon_1['end_date'] = datathon_1['end_date'].isoformat()
    assert json.loads(response.data.decode('UTF-8')) == [datathon_1]
    assert response.status_code == 200
    assert response.mimetype == 'application/json'


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonListUseCase')
def test_get_failed_response(mock_use_case, client):
    response_failure = res.ResponseFailure.build_system_error('test message')
    mock_use_case().execute.return_value = response_failure

    response = client.get('/datathons')

    assert json.loads(response.data.decode('utf-8')) == {
        'type': 'SystemError',
        'message': 'test message',
    }
    assert response.status_code == 500
    assert response.mimetype == 'application/json'


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonListUseCase')
def test_request_object_init_and_usage_with_filters(mock_use_case, client):
    mock_use_case().execute.return_value = res.ResponseSuccess([])
    request_object = mock.Mock()

    ro = 'datacontest.use_cases.request_objects.DatathonListRequestObject'
    with mock.patch(ro) as mock_request_object:
        mock_request_object.from_dict.return_value = request_object
        client.get('/datathons?filter_param1=value1&filter_param2=value2')

        mock_request_object.from_dict.assert_called_with(
            {'filters': {'param1': 'value1', 'param2': 'value2'}}
        )
        mock_use_case().execute.assert_called_with(request_object)
