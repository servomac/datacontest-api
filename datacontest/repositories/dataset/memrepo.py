from datacontest.domain import models
from datacontest.repositories import memrepo


class DatasetMemRepo(memrepo.MemRepo):
    domain_model = models.Dataset
