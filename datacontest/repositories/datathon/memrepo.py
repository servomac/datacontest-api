from datacontest.domain import models
from datacontest.repositories import memrepo


class DatathonMemRepo(memrepo.MemRepo):
    domain_model = models.Datathon
