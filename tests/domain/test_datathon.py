import datetime
import uuid
from datacontest.domain import models


def test_datathon_model_init():
    identifier = uuid.uuid4()
    datathon = models.Datathon(
        id=identifier,
        title='Title',
        subtitle='Subtitle',
        description='Some extense description',
        metric='AUC',
        end_date=datetime.datetime(2018, 1, 5, 13, 15, 0, 0),
    )

    assert datathon.id == identifier
    assert datathon.title == 'Title'
    assert datathon.subtitle == 'Subtitle'
    assert datathon.description == 'Some extense description'
    assert datathon.metric == 'AUC'
    assert datathon.end_date == datetime.datetime(2018, 1, 5, 13, 15, 0, 0)


def test_datathon_model_from_dict():
    identifier = uuid.uuid4()
    datathon = models.Datathon.from_dict({
        'id': identifier,
        'title': 'Title',
        'subtitle': 'Subtitle',
        'description': 'Some extense description',
        'metric': 'AUC',
        'end_date': datetime.datetime(2018, 1, 5, 13, 15, 0, 0)
    })

    assert datathon.id == identifier
    assert datathon.title == 'Title'
    assert datathon.subtitle == 'Subtitle'
    assert datathon.description == 'Some extense description'
    assert datathon.metric == 'AUC'
    assert datathon.end_date == datetime.datetime(2018, 1, 5, 13, 15, 0, 0)
