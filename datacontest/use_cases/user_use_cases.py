from datacontest.shared import use_case as uc
from datacontest.shared import response_object as res


class UserRegistrationUseCase(uc.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def email_already_exists(self, email):
        users_with_same_email = self.repo.list(filters={'email': email})
        return len(users_with_same_email) > 0

    def process_request(self, request_object):

        if self.email_already_exists(request_object.email):
            return res.ResponseFailure.build_authentication_error(
                'This email is already in use'
            )

        identifier = self.repo.build_primary_key()
        domain_user = self.repo.add(
            id=identifier,
            username=request_object.username,
            password=request_object.password,
            email=request_object.email,
        )

        return res.ResponseCreationSuccess(domain_user)


class UserLoginUseCase(uc.UseCase):
    pass


class UserLogoutUseCase(uc.UseCase):
    pass
