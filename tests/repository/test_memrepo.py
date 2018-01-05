import datetime
import pytest

from datacontest.shared.domain_model import DomainModel
from datacontest.repositories import memrepo


datathon_1 = {
    'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
    'title': 'Title1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
    'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
}

datathon_2 = {
    'id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    'title': 'Title2',
    'subtitle': 'Subtitle2',
    'description': 'Description2',
    'metric': 'AUC',
    'end_date': datetime.datetime(2018, 1, 5, 20, 15, 0, 0),
}

datathon_3 = {
    'id': 'g23236a4-5085-41e9-86dc-29d6923010s6',
    'title': 'Title3',
    'subtitle': 'Subtitle3',
    'description': 'Description3',
    'metric': 'accuracy',
    'end_date': datetime.datetime(2019, 1, 5, 20, 15, 0, 0),
}

@pytest.fixture
def datathons():
    return [datathon_1, datathon_2, datathon_3]


def _check_results(domain_models_list, data_list):
    assert len(domain_models_list) == len(data_list)
    assert all([isinstance(dm, DomainModel) for dm in domain_models_list])
    assert set([dm.id for dm in domain_models_list]) == set([d['id'] for d in data_list])


def test_repository_list_without_parameters(datathons):
    repo = memrepo.MemRepo(datathons)

    assert repo.list() == datathons


def test_repository_list_with_invalid_params(datathons):
    repo = memrepo.MemRepo(datathons)

    with pytest.raises(KeyError):
        repo.list(filters={'false': 'wrong'})


def test_repository_list_with_filters_unknown_operator(datathons):
    repo = memrepo.MemRepo(datathons)

    with pytest.raises(ValueError):
        repo.list(filters={'metric__in': ['AUC', 'accuracy']})


def test_repository_list_with_filters_end_date(datathons):
    repo = memrepo.MemRepo(datathons)

    date = datetime.datetime(2018, 1, 5, 20, 15, 0, 0)
    _check_results(repo.list(filters={'end_date': date}), [datathon_2])
    _check_results(repo.list(filters={'end_date__eq': date}), [datathon_2])
    _check_results(repo.list(filters={'end_date__gt': date}), [datathon_3])
    _check_results(repo.list(filters={'end_date__lt': date}), [datathon_1])


def test_repository_list_with_filters_id(datathons):
    repo = memrepo.MemRepo(datathons)

    _check_results(
        repo.list(filters={'id': '91090b75-65e9-4253-975c-6f8ad0eaa955'}),
        [datathon_1],
    )
