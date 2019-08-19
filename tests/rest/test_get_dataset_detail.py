import datetime
import json

from unittest import mock

from freezegun import freeze_time

from datacontest.domain.models import User, Datathon, Dataset


API_ENDPOINT = '/datathons/{datathon_id}/dataset'


@freeze_time('2018-01-01')
@mock.patch('datacontest.repositories.dataset.memrepo.DatasetMemRepo.find_by')
@mock.patch('datacontest.repositories.datathon.memrepo.DatathonMemRepo.find_by_id')
@mock.patch('datacontest.rest.decorators.jwt_current_identity')
def test_datathon_dataset_detail_as_organizer(mock_jwt_identity, mock_mem_repo, mock_dataset_mem_repo, client):
    mock_dataset_mem_repo.return_value = [Dataset.from_dict({
        'id': 'dataset_id',
        'datathon_id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'training': 'any',
        'validation': 'any',
        'test': 'any',
        'target_column': 'target_column',
    })]
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

    organizer_mock = User('f4b236a4-5085-41e9-86dc-29d6923010b3', 'user', 'pass', 'email@email.com')
    mock_jwt_identity.return_value = organizer_mock

    response = client.get(
        API_ENDPOINT.format(datathon_id='91090b75-65e9-4253-975c-6f8ad0eaa955'),
        headers={'Authorization': 'Bearer any'},
        content_type='application/json'
    )

    #mock_dataset_mem_repo.assert_called_with('datathon_id', '91090b75-65e9-4253-975c-6f8ad0eaa955')
    #mock_mem_repo.assert_called_with('91090b75-65e9-4253-975c-6f8ad0eaa955')
    assert json.loads(response.data) == [{
        'datathon_id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
        'id': 'dataset_id',
        'test': 'any',
        'training': 'any',
        'validation': 'any',
        'target_column': 'target_column',
    }]
    assert response.status_code == 200


# TODO unauthenticated
# TODO unexistent datathon
# TODO as non organizer
# TODO as non organizer when the datathon has ended
# TODO as non organizer when there is no dataset