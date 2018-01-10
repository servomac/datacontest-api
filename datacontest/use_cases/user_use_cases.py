import uuid

from datacontest.shared import use_case as uc
from datacontest.shared import response_object as res


class UserRegistrationUseCase(uc.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        users_with_same_email = self.repo.list(
            filters={'email': request_object.email})
        if len(users_with_same_email) > 0:
            return res.ResponseFailure.build_authentication_error('This email is already in use')


        domain_user = self.repo.add(
            id=uuid.uuid4(),
            username=request_object.username,
            password=request_object.password,
            email=request_object.email)

        if domain_user is None:
            return res.ResponseFailure()

        return res.ResponseSuccess(domain_user)


class UserLoginUseCase:
    pass


class UserLogoutUseCase:
    pass
