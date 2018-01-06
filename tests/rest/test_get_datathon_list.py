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
    'end_date': datetime.datetime(2018, 1, 5, 18, 20, 9, 910076) 
}

datathons = [Datathon.from_dict(datathon_1)]


@mock.patch('datacontest.use_cases.datathon_use_cases.DatathonListUseCase')
def test_get(mock_use_case, client):
    mock_use_case().execute.return_value = res.ResponseSuccess(datathons)

    response = client.get('/datathons')

    datathon_1['end_date'] = datathon_1['end_date'].isoformat()
    assert json.loads(response.data.decode('UTF-8')) == [datathon_1]
    assert response.status_code == 200
    assert response.mimetype == 'application/json'
