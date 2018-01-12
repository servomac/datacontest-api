import datetime
import json

from datacontest.serializers import user_serializer as serializer
from datacontest.domain import models


def test_serialize_user_model():
    user = models.User(
        'bdae3b21-4577-4e2f-a825-bbbc1aeb7c49',
        username='Username',
        password='password',
        email='Email',
        created_at=datetime.datetime(2017, 1, 5, 13, 15, 0, 0),
        is_admin=False,
    )

    expected_json = """
        {
            "id": "bdae3b21-4577-4e2f-a825-bbbc1aeb7c49",
            "username": "Username",
            "email": "Email",
            "created_at": "2017-01-05T13:15:00"
        }
    """

    serialized = json.dumps(user, cls=serializer.UserEncoder)
    assert json.loads(serialized) == json.loads(expected_json)
