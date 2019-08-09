import datetime
import pytest

from datacontest.shared.domain_model import DomainModel
from datacontest.repositories.datathon import memrepo


datathon_1 = {
    'id': '91090b75-65e9-4253-975c-6f8ad0eaa955',
    'title': 'Title1',
    'subtitle': 'Subtitle1',
    'description': 'Description1',
    'metric': 'AUC',
    'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
    'organizer_id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
}

datathon_2 = {
    'id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
    'title': 'Title2',
    'subtitle': 'Subtitle2',
    'description': 'Description2',
    'metric': 'AUC',
    'end_date': datetime.datetime(2018, 1, 5, 20, 15, 0, 0),
    'organizer_id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
}

datathon_3 = {
    'id': 'g23236a4-5085-41e9-86dc-29d6923010s6',
    'title': 'Title3',
    'subtitle': 'Subtitle3',
    'description': 'Description3',
    'metric': 'accuracy',
    'end_date': datetime.datetime(2019, 1, 5, 20, 15, 0, 0),
    'organizer_id': 'f4b236a4-5085-41e9-86dc-29d6923010b3',
}


@pytest.fixture
def datathons():
    return [datathon_1, datathon_2, datathon_3]


def _check_results(domain_models_list, data_list):
    assert len(domain_models_list) == len(data_list)
    assert all([isinstance(dm, DomainModel) for dm in domain_models_list])

    domain_model_ids = set([m.id for m in domain_models_list])
    assert domain_model_ids == set([d['id'] for d in data_list])


def test_repository_build_primary_key():
    repo = memrepo.DatathonMemRepo([])

    pk1 = repo.build_primary_key()
    pk2 = repo.build_primary_key()

    assert isinstance(pk1, str) and isinstance(pk2, str)
    assert pk1 != pk2
    assert len(pk1) == len(pk2)


def test_repository_list_without_parameters(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    assert repo.list() == datathons


def test_repository_list_with_invalid_params(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    with pytest.raises(KeyError):
        repo.list(filters={'false': 'wrong'})


def test_repository_list_with_filters_unknown_operator(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    with pytest.raises(ValueError):
        repo.list(filters={'metric__in': ['AUC', 'accuracy']})


def test_repository_list_with_filters_end_date(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    date = datetime.datetime(2018, 1, 5, 20, 15, 0, 0)
    _check_results(repo.list(filters={'end_date': date}), [datathon_2])
    _check_results(repo.list(filters={'end_date__eq': date}), [datathon_2])
    _check_results(repo.list(filters={'end_date__gt': date}), [datathon_3])
    _check_results(repo.list(filters={'end_date__lt': date}), [datathon_1])


def test_repository_list_with_filters_id(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    _check_results(
        repo.list(filters={'id': '91090b75-65e9-4253-975c-6f8ad0eaa955'}),
        [datathon_1],
    )

def test_find_by_id_success(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    domain_model = repo.find_by_id('g23236a4-5085-41e9-86dc-29d6923010s6')
    assert isinstance(domain_model, DomainModel)
    assert domain_model.id == datathon_3['id']
    assert domain_model.description == datathon_3['description']


def test_find_by_id_failure(datathons):
    repo = memrepo.DatathonMemRepo(datathons)

    assert repo.find_by_id('nonexistent') is None


#TODO def test_add_success / failure(datathons):
