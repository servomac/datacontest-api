from datacontest.shared import response_object as res


STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseCreationSuccess.CREATION_SUCCESS: 201,
    res.ResponseFailure.AUTHORIZATION_ERROR: 401,   # AUTHENTICATION! TODO
    res.ResponseFailure.AUTHENTICATION_ERROR: 403,  # AUTHORIZATION
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.SYSTEM_ERROR: 500,
}
