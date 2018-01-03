class Datathon:
    def __init__(self, id, title, subtitle, description, metric):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.metric = metric

    @classmethod
    def from_dict(cls, data):
        return Datathon(
            id=data['id'],
            title=data['title'],
            subtitle=data['subtitle'],
            description=data['description'],
            metric=data['metric'],
        )
