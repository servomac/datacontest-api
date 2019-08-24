from functools import wraps
import json

from flask import Response, request

from datacontest.shared import response_object as res
from datacontest.rest.jwt import jwt_current_identity
from datacontest.rest.jwt import JWTException, JWT_HEADER
from datacontest.rest.user import user_repo
from datacontest.rest.utils import STATUS_CODES


def login_required(f):
    """
     - Obtain the user associated to the provided Authentication header JWT token.
     - and inject the user to the wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return Response(
                json.dumps({
                    'type': res.ResponseFailure.PARAMETERS_ERROR,
                    'message': 'Request body must be JSON.',
                }),
                mimetype='application/json',
                status=STATUS_CODES[res.ResponseFailure.PARAMETERS_ERROR]
            )

        try:
            access_token = request.headers.get(JWT_HEADER)
            user = jwt_current_identity(user_repo, access_token)
        except JWTException as e:
            return Response(
                json.dumps({
                    'type': res.ResponseFailure.AUTHORIZATION_ERROR,
                    'message': str(e),
                }),
                mimetype='application/json',
                status=STATUS_CODES[res.ResponseFailure.AUTHORIZATION_ERROR]
            )

        if user is None:
            return Response(
                json.dumps({
                    'type': res.ResponseFailure.AUTHORIZATION_ERROR,
                    'message': 'User not found!',
                }),
                mimetype='application/json',
                status=STATUS_CODES[res.ResponseFailure.AUTHORIZATION_ERROR]
            )

        return f(user, *args, **kwargs)
    return decorated_function
