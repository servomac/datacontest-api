class MemRepo:

    def __init__(self, entries=None):
        self._entries = []
        if entries:
            self._entries.extend(entries)

    def build_primary_key(self):
        import uuid
        return str(uuid.uuid4())

    def _check(self, element, key, value):
        if '__' not in key:
            key = key + '__eq'

        key, operator = key.split('__')

        if operator not in ['eq', 'lt', 'gt']:
            raise ValueError('Operator {} is not supported'.format(operator))

        operator = '__{}__'.format(operator)

        return getattr(element[key], operator)(value)

    def list(self, filters=None):
        if not filters:
            return self._entries

        result = []
        result.extend(self._entries)

        for key, value in filters.items():
            result = [e for e in result if self._check(e, key, value)]

        return [self.domain_model.from_dict(e) for e in result]

    def find_by(self, key, value):
        return [
            self.domain_model.from_dict(e)
            for e in self._entries
            if e[key] == value
        ]

    def add(self, **kwargs):
        self._entries.append(kwargs)
        return self.domain_model.from_dict(kwargs)
