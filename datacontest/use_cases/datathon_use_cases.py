from datacontest.shared import use_case as uc
from datacontest.shared import response_object as res


class DatathonListUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_datathons = self.repo.list(filters=request_object.filters)
        return res.ResponseSuccess(domain_datathons)
