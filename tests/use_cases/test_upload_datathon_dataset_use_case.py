from unittest import mock

from datacontest.shared import response_object as res
from datacontest.use_cases import request_objects as req
from datacontest.use_cases import datathon_use_cases as uc


def test_upload_datathon_datset_use_case_without_parameters():
    datathon_repo = mock.Mock()
    dataset_repo = mock.Mock()

    user_login_use_case = uc.UploadDatathonDataset(datathon_repo, dataset_repo)
    request_object = req.UploadDatathonDatasetRequestObject.from_dict({})

    response_object = user_login_use_case.execute(request_object)

    # TODO aixo no m'agrada perque estic responent a l'usuari que necessita introduir user_id quan no és vera
    # estic 'leacking' informació interna de paràmetres de l'API del request object, quan l'usuari final del
    # l'api rest enviarà un token, no el seu user_id... revisar!
    assert bool(response_object) is False
    assert response_object.value == {
        'message': 'datathon_id: Its a mandatory parameter!\n'
                   'user_id: Its a mandatory parameter!\n'
                   'training: Its a mandatory parameter!\n'
                   'validation: Its a mandatory parameter!\n'
                   'test: Its a mandatory parameter!\n'
                   'target_column: Its a mandatory parameter!',
        'type': res.ResponseFailure.PARAMETERS_ERROR,
    }


# def test_user_login_use_case_unexistent_user():
#     repo = mock.Mock()
#     repo.list.return_value = []

#     user_login_use_case = uc.UserLoginUseCase(repo)
#     request_object = req.UserLoginRequestObject.from_dict({
#         'username': 'unexistent',
#         'password': 'pass',
#     })

#     response_object = user_login_use_case.execute(request_object)

#     repo.list.assert_called_with(filters={'username': 'unexistent'})
#     assert bool(response_object) is False
#     assert response_object.value == {
#         'message': 'User not found!',
#         'type': res.ResponseFailure.RESOURCE_ERROR,
#     }


# def test_user_login_use_case_invalid_password():
#     mocked_user = mock.Mock()
#     mocked_user.is_valid_password.return_value = False

#     repo = mock.Mock()
#     repo.list.return_value = [mocked_user]

#     user_login_use_case = uc.UserLoginUseCase(repo)
#     request_object = req.UserLoginRequestObject.from_dict({
#         'username': 'any_user',
#         'password': 'any_pass',
#     })

#     response_object = user_login_use_case.execute(request_object)

#     repo.list.assert_called_with(filters={'username': 'any_user'})
#     mocked_user.is_valid_password.assert_called_with('any_pass')

#     assert bool(response_object) is False
#     assert response_object.value == {
#         'message': 'Invalid password!',
#         'type': res.ResponseFailure.AUTHORIZATION_ERROR,
#     }


# def test_user_login_use_case_success():
#     mocked_user = mock.Mock()
#     mocked_user.is_valid_password.return_value = True

#     repo = mock.Mock()
#     repo.list.return_value = [mocked_user]

#     user_login_use_case = uc.UserLoginUseCase(repo)
#     request_object = req.UserLoginRequestObject.from_dict({
#         'username': 'any_user',
#         'password': 'any_pass',
#     })

#     response_object = user_login_use_case.execute(request_object)

#     repo.list.assert_called_with(filters={'username': 'any_user'})
#     mocked_user.is_valid_password.assert_called_with('any_pass')

#     assert bool(response_object) is True
#     assert response_object.value == mocked_user
