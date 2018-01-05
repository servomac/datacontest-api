import datetime
import json

from datacontest.serializers import datathon_serializer as serializer
from datacontest.domain import models


def test_serialize_datathon_model():
    datathon = models.Datathon('bdae3b21-4577-4e2f-a825-bbbc1aeb7c49',
                               title='Title',
                               subtitle='Subtitle',
                               description='An extense description',
                               metric='AUC',
                               end_date=datetime.datetime(2018, 1, 5, 13, 15, 0, 0))

    expected_json = """
        {
            "id": "bdae3b21-4577-4e2f-a825-bbbc1aeb7c49",
            "title": "Title",
            "subtitle": "Subtitle",
            "description": "An extense description",
            "metric": "AUC",
            "end_date": "2018-01-05T13:15:00"
        }
    """

    serialized = json.dumps(datathon, cls=serializer.DatathonEncoder)
    assert json.loads(serialized) == json.loads(expected_json)
