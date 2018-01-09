import json


class UserEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return {
                'id': o.id,
                'username': o.username,
                'email': o.email,
                'created_at': o.created_at.isoformat(),
            }
        except AttributeError:
            return super().default(o)
