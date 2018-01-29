import json

from flask import Blueprint, Response, request

from datacontest.repositories.datathon import memrepo
from datacontest.repositories.user import memrepo as user_memrepo
from datacontest.serializers import datathon_serializer
from datacontest.use_cases import datathon_use_cases as uc
from datacontest.use_cases import request_objects as req

from datacontest.shared import response_object as res
from datacontest.rest.jwt import jwt_current_identity
from datacontest.rest.jwt import JWTException
from datacontest.rest.utils import STATUS_CODES


blueprint = Blueprint('datathon', __name__)


@blueprint.route('/datathons', methods=['GET'])
def datathons():
    query_params = {
        'filters': {},
    }

    # TODO this parameter passing seems so obscure to mee
    # rethink, because it could be more semantic
    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            query_params['filters'][arg.replace('filter_', '')] = values

    request_object = req.DatathonListRequestObject.from_dict(query_params)

    repo = memrepo.DatathonMemRepo()
    use_case = uc.DatathonListUseCase(repo)

    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )


@blueprint.route('/datathons', methods=['POST'])
def create_datathon():
    args = request.get_json()

    user_repo = user_memrepo.UserMemRepo()
    try:
        user = jwt_current_identity(user_repo, args.get('access_token'))
    except JWTException as e:
        return Response(
            json.dumps({
                'type': res.ResponseFailure.AUTHORIZATION_ERROR,
                'message': str(e),
            }),
            mimetype='application/json',
            status=STATUS_CODES[res.ResponseFailure.AUTHORIZATION_ERROR]
        )

    request_object = req.CreateDatathonRequestObject(
        title=args.get('title'),
        description=args.get('description'),
        metric=args.get('metric'),
        end_date=args.get('end_date'),
        user=user,
    )

    repo = memrepo.DatathonMemRepo()
    use_case = uc.CreateDatathonUseCase(repo)

    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )


@blueprint.route('/datathons/<datathon_id>')
def datathon_detail(datathon_id):
    request_object = req.DatathonDetailRequestObject(datathon_id)

    repo = memrepo.DatathonMemRepo()
    use_case = uc.DatathonDetailUseCase(repo)

    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )
