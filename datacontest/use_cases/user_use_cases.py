from datacontest.shared import use_case as uc
from datacontest.shared import response_object as res


class UserRegistrationUseCase(uc.UseCase):
    def __init__(self, repo):
        self.repo = repo

    def _email_already_exists(self, email):
        users_with_same_email = self.repo.list(filters={'email': email})
        return len(users_with_same_email) > 0

    def process_request(self, request_object):

        if self._email_already_exists(request_object.email):
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
    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        """ If valid, returns the required user """
        users = self.repo.list(filters={'username': request_object.username})
        if len(users) != 1:
            return res.ResponseFailure.build_resource_error(
                'User not found!'
            )

        domain_user = users[0]
        if not domain_user.is_valid_password(request_object.password):
            return res.ResponseFailure.build_authorization_error(
                'Invalid password!'
            )

        return res.ResponseSuccess(domain_user)


class UserLogoutUseCase(uc.UseCase):
    pass
