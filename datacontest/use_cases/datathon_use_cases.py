from datacontest.shared import response_object as ro


class DatathonListUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request_object):
        datathons = self.repo.list()
        return ro.ResponseSuccess(datathons)
