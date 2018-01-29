from datetime import datetime, timedelta

import jwt


class JWTException(Exception):
    # TODO implement multiple errors
    pass


class JWTManager:

    def __init__(self, secret='aa', identity_field='id'):
        self.secret = secret
        self.identity_field = identity_field
        self.expiration_field = 'exp'

    def build_token(self, id, expiration_days=15):
        return self._generate_jwt_token(id, expiration_days)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret)
        except jwt.exceptions.DecodeError as e:
            raise JWTException('{}'.format(e))

        if payload.get(self.identity_field) is None:
            raise JWTException('The token should contain an identity field'
                               ' ({})'.format(self.identity_field))

        if payload.get(self.expiration_field) is None:
            raise JWTException('The token should contain an expiration field'
                               ' ({})'.format(self.expiration_field))

        return payload

    def get_identity(self, token):
        payload = self.decode_token(token)
        return payload.get(self.identity_field)

    def is_valid_token(self, token, id):
        return (
            self.get_identity(token) == id and
            self.is_expired_token(token) is False
        )

    def is_expired_token(self, token):
        payload = self.decode_token(token)

        return datetime.now() >= datetime.fromtimestamp(
            payload.get(self.expiration_field))

    def _generate_jwt_token(self, id, expiration_days):
        payload = {
            self.identity_field: id,
            self.expiration_field: datetime.utcnow() + timedelta(days=expiration_days),
        }

        token = jwt.encode(payload, self.secret)

        return token.decode('utf-8')


def jwt_current_identity(user_repo, access_token):
    """
    Given a user repository and an access token, returns the user
    if the access token is valid and the user exists, None otherwise.

    In case of invalid authorization, raises a JWTException.
    """
    if access_token is None:
        raise JWTException('No token provided.')

    jwt_manager = JWTManager()
    user_id = jwt_manager.get_identity(access_token)
    user = user_repo.find_by_id(user_id)

    return user
