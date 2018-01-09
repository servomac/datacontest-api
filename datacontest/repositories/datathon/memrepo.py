from datacontest.domain import models
from datacontest.repositories import memrepo

class DatathonMemRepo(memrepo.MemRepo):
    domain_model = models.Datathon

    def find_by_id(self, id):
        for datathon in self._entries:
            if datathon['id'] == id:
                return models.Datathon.from_dict(datathon)

        return None
