import pytest
from unittest import mock

from datacontest.domain import models
from datacontest.use_cases import datathon_use_cases as uc


@pytest.fixture
def domain_datathons():
    datathon_1 = models.Datathon('91090b75-65e9-4253-975c-6f8ad0eaa955',
                                 title='Title1',
                                 subtitle='Subtitle1',
                                 description='Description1',
                                 metric='AUC')
    
    datathon_2 = models.Datathon('f4b236a4-5085-41e9-86dc-29d6923010b3',
                                 title='Title2',
                                 subtitle='Subtitle2',
                                 description='Description2',
                                 metric='AUC')

    return [datathon_1, datathon_2]


def test_datathon_list_without_parameters(domain_datathons):
    repo = mock.Mock()
    repo.list.return_value = domain_datathons

    datathon_list_use_case = uc.DatathonListUseCase(repo)
    result = datathon_list_use_case.execute()

    repo.list.assert_called_with()
    assert result == domain_datathons
