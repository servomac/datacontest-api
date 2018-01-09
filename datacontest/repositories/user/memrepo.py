from datacontest.repositories import memrepo

class UserMemRepo(memrepo.MemRepo):
    domain_model = models.User
