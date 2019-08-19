import json

from flask import Blueprint, Response, request

from datacontest.repositories.dataset import memrepo as dataset_memrepo
from datacontest.repositories.datathon import memrepo as datathon_memrepo
from datacontest.serializers import datathon_serializer, dataset_serializer
from datacontest.use_cases import datathon_use_cases as datathon_uc
from datacontest.use_cases import dataset_use_cases as dataset_uc
from datacontest.use_cases import request_objects as req

from datacontest.shared import response_object as res
from datacontest.rest.decorators import login_required
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

    repo = datathon_memrepo.DatathonMemRepo()
    use_case = datathon_uc.DatathonListUseCase(repo)

    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )


@blueprint.route('/datathons', methods=['POST'])
@login_required
def create_datathon(user):
    args = request.get_json()
    args_and_user = {**args, **{'organizer_id': user.id}}

    request_object = req.CreateDatathonRequestObject.from_dict(args_and_user)
    if bool(request_object) is False:
        return Response(json.dumps(request_object.errors))

    repo = datathon_memrepo.DatathonMemRepo()
    use_case = datathon_uc.CreateDatathonUseCase(repo)

    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )


@blueprint.route('/datathons/<datathon_id>')
def datathon_detail(datathon_id):
    request_object = req.DatathonDetailRequestObject(datathon_id)
    if bool(request_object) is False:
        # TODO status code
        return Response(json.dumps(request_object.errors))

    repo = datathon_memrepo.DatathonMemRepo()
    use_case = datathon_uc.DatathonDetailUseCase(repo)

    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=datathon_serializer.DatathonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type]
    )


@blueprint.route('/datathons/<datathon_id>/dataset', methods=['POST'])
@login_required
def upload_datathon_dataset(user, datathon_id):
    args = request.get_json()
    args_and_user = {**args, **{'user_id': user.id, 'datathon_id': datathon_id}}

    request_object = req.UploadDatathonDatasetRequestObject.from_dict(args_and_user)
    if bool(request_object) is False:
        # TODO return Encoder for failure request?
        return Response(
            json.dumps(request_object.errors),
            mimetype='application/json',
            status=STATUS_CODES[res.ResponseFailure.PARAMETERS_ERROR]
        )

    datathon_repo = datathon_memrepo.DatathonMemRepo()
    dataset_repo = dataset_memrepo.DatasetMemRepo()
    use_case = dataset_uc.UploadDatathonDataset(datathon_repo, dataset_repo)

    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=dataset_serializer.DatasetEncoder),
        mimetype='application/json',
        status=STATUS_CODES[response.type],
    )


# @blueprint.route('/datathons/<datathon_id>/', method="POST")
# def datathon_subscription_or_update(datathon_id):
#     """
#     Endpoint representing different semantics depending on the user:
#      - The organizer can update the datathon.
#      - An user can join the competition while it's open.
#     """
#     pass



# @blueprint.route('/datathons/<datathon_id>/', method="DELETE")
# def datathon_delete(datathon_id):
#    pass
