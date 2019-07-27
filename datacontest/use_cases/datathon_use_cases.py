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


class CreateDatathonUseCase(uc.UseCase):

    def __init__(self, repo):
        # TODO add user repo?
        self.repo = repo

    def process_request(self, request_object):
        # TODO user authentication?
        identifier = self.repo.build_primary_key()
        domain_datathon = self.repo.add(id=identifier,
                                        title=request_object.title,
                                        subtitle=request_object.subtitle,
                                        description=request_object.description,
                                        metric=request_object.metric,
                                        organizer_id=request_object.organizer_id,
                                        end_date=request_object.end_date)

        return res.ResponseCreationSuccess(domain_datathon)
