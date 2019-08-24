import json


class DatasetEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return {
                'id': o.id,
                'datathon_id': o.datathon_id,
                'training': o.training,
                'validation': o.validation,
                'test': o.test,
                'target_column': o.target_column,
            }
        except AttributeError:
            return super().default(o)
