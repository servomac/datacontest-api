from datetime import datetime, timedelta

import jwt


class JWTManager:

    def __init__(self, secret='aa', identity_field='id', expiration_field='exp'):
        self.secret = secret
        self.identity_field = identity_field
        self.expiration_field = expiration_field

    def build_token(self, id, expiration_days=15):
        return self._generate_jwt_token(id, expiration_days)

    def decode_token(self, token):
        return jwt.decode(token, self.secret)

    def is_valid_token(self, token, id):
        payload = self.decode_token(token)

        return (
            payload.get(self.identity_field) == id and
            self.is_expired_token(token) is False
        )
    
    def is_expired_token(self, token):
        payload = self.decode_token(token)

        return datetime.datetime.now() < datetime.fromtimestamp(
            payload.get(self.expiration_field))

    def _generate_jwt_token(self, id, expiration_days):
        payload = {
            self.identity_field: id,
            self.expiration_field: datetime.utcnow() + timedelta(days=expiration_days),
        }

        token = jwt.encode(payload, self.secret)

        return token.decode('utf-8')
