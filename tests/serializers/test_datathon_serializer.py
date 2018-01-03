import json

from datacontest.serializers import datathon_serializer as serializer
from datacontest.domain import models


def test_serialize_datathon_model():
    datathon = models.Datathon('bdae3b21-4577-4e2f-a825-bbbc1aeb7c49',
                               title='Title',
                               subtitle='Subtitle',
                               description='An extense description',
                               metric='AUC')

    expected_json = """
        {
            "id": "bdae3b21-4577-4e2f-a825-bbbc1aeb7c49",
            "title": "Title",
            "subtitle": "Subtitle",
            "description": "An extense description",
            "metric": "AUC"
        }
    """

    serialized = json.dumps(datathon, cls=serializer.DatathonEncoder)
    assert json.loads(serialized) == json.loads(expected_json)
