import json


class DatathonEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return {
                'id': o.id,
                'title': o.title,
                'subtitle': o.subtitle,
                'description': o.description,
                'metric': o.metric,
                'end_date': o.end_date.isoformat(),
                'organizer_id': o.organizer_id,
            }
        except AttributeError:
            return super().default(o)
