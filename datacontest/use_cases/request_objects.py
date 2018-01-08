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
