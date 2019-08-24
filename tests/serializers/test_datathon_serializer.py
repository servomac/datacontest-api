import datetime
import json

from datacontest.serializers import datathon_serializer as serializer
from datacontest.domain import models


def test_serialize_datathon_model():
    datathon = models.Datathon(
        'bdae3b21-4577-4e2f-a825-bbbc1aeb7c49',
        title='Title',
        subtitle='Subtitle',
        description='An extense description',
        metric='AUC',
        start_date=datetime.datetime(2018, 1, 5, 10, 15, 0, 0),
        end_date=datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
        organizer_id='971ce791-489b-46ab-ae78-a5eca3beaa5a',
    )

    expected_json = """
        {
            "id": "bdae3b21-4577-4e2f-a825-bbbc1aeb7c49",
            "title": "Title",
            "subtitle": "Subtitle",
            "description": "An extense description",
            "metric": "AUC",
            "start_date": "2018-01-05T10:15:00",
            "end_date": "2018-01-05T13:15:00",
            "organizer_id": "971ce791-489b-46ab-ae78-a5eca3beaa5a"
        }
    """

    serialized = json.dumps(datathon, cls=serializer.DatathonEncoder)
    assert json.loads(serialized) == json.loads(expected_json)
