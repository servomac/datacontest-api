from datacontest.shared import response_object as res
from datacontest.shared import use_case as uc


class DatathonListUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_datathons = self.repo.list(filters=request_object.filters)
        return res.ResponseSuccess(domain_datathons)


class DatathonDetailUseCase(uc.UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        domain_datathon = self.repo.find_by_id(request_object.id)
        if domain_datathon is None:
            return res.ResponseFailure.build_resource_error('Id not found')

        return res.ResponseSuccess(domain_datathon)
