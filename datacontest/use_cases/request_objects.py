import collections


class InvalidRequestObject:

    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        return len(self.errors) > 0

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidRequestObject:

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class DatathonListRequestObject(ValidRequestObject):

    def __init__(self, filters=None):
        self.filters = filters

    @classmethod
    def from_dict(cls, data):
        invalid_req = InvalidRequestObject()

        if 'filters' in data and \
           not isinstance(data['filters'], collections.Mapping):
            invalid_req.add_error('filters', 'Is not iterable')

        if invalid_req.has_errors():
            return invalid_req

        return DatathonListRequestObject(filters=data.get('filters', None))

    def __nonzero__(self):
        return True
