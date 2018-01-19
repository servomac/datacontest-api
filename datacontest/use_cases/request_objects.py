# TODO extract the schema validation, use some existing library
# i.e. in both registration and login objects exists duplicated code

import collections

from datacontest.shared import request_object as req


class DatathonListRequestObject(req.ValidRequestObject):

    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        if 'filters' in data and \
           not isinstance(data['filters'], collections.Mapping):
            invalid_req.add_error('filters', 'Is not iterable')

        if invalid_req.has_errors():
            return invalid_req

        return DatathonListRequestObject(filters=data.get('filters', None))

    def __nonzero__(self):
        return True


class DatathonDetailRequestObject(req.ValidRequestObject):

    def __init__(self, id):
        self.id = id

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        if 'id' not in data:
            invalid_req.add_error('id', 'Its a mandatory parameter!')

        if 'id' in data and not cls._valid_id(data['id']):
            invalid_req.add_error('id', 'Should be a valid uuid.')

        if invalid_req.has_errors():
            return invalid_req

        return DatathonDetailRequestObject(id=data['id'])

    @staticmethod
    def _valid_id(id):
        return isinstance(id, str)

    def __nonzero__(self):
        return True


class CreateDatathonRequestObject(req.ValidRequestObject):

    def __init__(self, title, description, metric, organizer_id, end_date):
        self.title = title
        self.description = description
        self.metric = metric
        self.organizer_id = organizer_id
        self.end_date = end_date

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        # TODO change this custom and naive schema validation..
        required_args = [('organizer_id', int), ('title', str), ('description', str)]
        for arg, arg_type in required_args:
            if arg not in data:
                invalid_req.add_error(arg, 'Its a mandatory parameter!')
            elif not isinstance(data[arg], arg_type):
                invalid_req.add_error(arg, 'Must be a {}.'.format(arg_type.__name__))

        optional_args = ['metric', 'end_date']
        for arg in optional_args:
            if not isinstance(data.get(arg), str):
                invalid_req.add_error(arg, 'Must be a string.')

        # TODO format de end date? inspirarme en altres serializers

        if invalid_req.has_errors():
            return invalid_req

        return CreateDatathonRequestObject(
            title=data['title'],
            description=data['description'],
            metric=data.get('metric'),
            organizer_id=data['organizer_id'],
            end_date=data.get('end_date'),
        )


class UserRegistrationRequestObject(req.ValidRequestObject):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        required_args = ['username', 'password', 'email']
        for arg in required_args:
            if arg not in data:
                invalid_req.add_error(arg, 'Its a mandatory parameter!')
            elif not isinstance(data[arg], str):
                invalid_req.add_error(arg, 'Must be a string.')

        if invalid_req.has_errors():
            return invalid_req

        return UserRegistrationRequestObject(
            username=data['username'],
            password=data['password'],
            email=data['email'],
        )

    def __nonzero__(self):
        return True


class UserLoginRequestObject(req.ValidRequestObject):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        required_args = ['username', 'password']
        for arg in required_args:
            if arg not in data:
                invalid_req.add_error(arg, 'Its a mandatory parameter!')
            elif not isinstance(data[arg], str):
                invalid_req.add_error(arg, 'Must be a string.')

        if invalid_req.has_errors():
            return invalid_req

        return UserLoginRequestObject(
            username=data['username'],
            password=data['password'],
        )
