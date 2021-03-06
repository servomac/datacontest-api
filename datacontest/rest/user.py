import json

from flask import Blueprint, Response, request

from datacontest.repositories.user import memrepo
from datacontest.serializers import user_serializer
from datacontest.use_cases import user_use_cases as uc
from datacontest.use_cases import request_objects as req

from datacontest.rest.jwt import JWTManager
from datacontest.rest.utils import STATUS_CODES

blueprint = Blueprint('user', __name__)
jwt = JWTManager()

user_repo = memrepo.UserMemRepo()

@blueprint.route('/user/registration', methods=['POST'])
def register():
    args = request.get_json()

    request_object = req.UserRegistrationRequestObject.from_dict(args)
    if bool(request_object) is False:
        return Response(json.dumps(request_object.errors))

    use_case = uc.UserRegistrationUseCase(user_repo)

    response = use_case.execute(request_object)

    if bool(response) is True:
        body = json.dumps(response.value, cls=user_serializer.UserEncoder)
    else:
        body = json.dumps(response.value)

    return Response(body,
                    mimetype='application/json',
                    status=STATUS_CODES[response.type])


@blueprint.route('/user/login', methods=['POST'])
def login():
    args = request.get_json()

    request_object = req.UserLoginRequestObject.from_dict(args)
    if bool(request_object) is False:
        return Response(json.dumps(request_object.errors))

    use_case = uc.UserLoginUseCase(user_repo)

    response = use_case.execute(request_object)
    if bool(response) is True:
        user = response.value
        body = {'access_token': jwt.build_token(user.id)}
    else:
        body = response.value

    return Response(json.dumps(body),
                    mimetype='application/json',
                    status=STATUS_CODES[response.type])


def logout():
    pass


# TODO refresh