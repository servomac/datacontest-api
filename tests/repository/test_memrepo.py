import pytest

from datacontest.repositories import memrepo


datathon_1 = {
    'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
    'title': 'Title1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
}

datathon_2 = {
    'id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    'title': 'Title2',
    'subtitle': 'Subtitle2',
    'description': 'Description2',
    'metric': 'AUC',
}

@pytest.fixture
def datathons():
    return [datathon_1, datathon_2]


def _check_results(domain_models_list, data_lists):
    assert len(domain_models_list) == len(data_list)
    assert all([isinstance(dm, DomainModel) for dm in domain_models_list])
    assert set([dm.code for dm in domain_models_list]) == set([d['code'] for d in data_list])


def test_repository_list_without_parameters(datathons):
    repo = memrepo.MemRepo(datathons)

    assert repo.list() == datathons
