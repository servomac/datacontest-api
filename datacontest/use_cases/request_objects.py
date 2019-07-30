# TODO extract the schema validation, use some existing library
# i.e. in both registration and login objects exists duplicated code

import collections
from datetime import datetime

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
    EXPECTED_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
    VALID_METRICS = ('AUC', 'ACCURACY', 'RMSE', 'RSE',)

    def __init__(self, title, subtitle, description, metric, organizer_id, end_date):
        self.title = title
        self.subtitle = subtitle or ''
        self.description = description
        self.metric = metric or 'AUC'
        self.organizer_id = organizer_id
        self.end_date = end_date

    @classmethod
    def from_dict(cls, data):
        invalid_req = req.InvalidRequestObject()

        # TODO change this custom and naive schema validation..
        required_args = [('organizer_id', str), ('title', str), ('description', str)]
        for arg, arg_type in required_args:
            if arg not in data:
                invalid_req.add_error(arg, 'Its a mandatory parameter!')
            elif not isinstance(data[arg], arg_type):
                invalid_req.add_error(arg, 'Must be a {}.'.format(arg_type.__name__))

        optional_args = ['metric', 'end_date', 'subtitle']
        for arg in optional_args:
            if arg in data and not isinstance(data.get(arg), str):
                invalid_req.add_error(arg, 'Must be a string.')

        if 'end_date' in data and isinstance(data['end_date'], str):
            try:
                data['end_date'] = datetime.strptime(
                    data['end_date'],
                    cls.EXPECTED_DATETIME_FORMAT,
                )
            except ValueError as ex:
                invalid_req.add_error('end_date', 'Must be a valid ISO 8601')

        if 'metric' in data and isinstance(data['metric'], str):
            if data['metric'] not in cls.VALID_METRICS:
                invalid_req.add_error(
                    'metric',
                    f"Must be a valid metric ({','.join(cls.VALID_METRICS)})."
                )

        if invalid_req.has_errors():
            return invalid_req

        return CreateDatathonRequestObject(
            title=data['title'],
            subtitle=data.get('subtitle', None),
            description=data['description'],
            metric=data.get('metric', None),
            organizer_id=data['organizer_id'],
            end_date=data.get('end_date', None),
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
