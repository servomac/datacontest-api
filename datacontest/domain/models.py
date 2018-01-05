from datacontest.shared.domain_model import DomainModel


class Datathon:
    def __init__(self, id, title, subtitle, description, metric, end_date):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.metric = metric
        self.end_date = end_date

    @classmethod
    def from_dict(cls, data):
        return Datathon(
            id=data['id'],
            title=data['title'],
            subtitle=data['subtitle'],
            description=data['description'],
            metric=data['metric'],
            end_date=data['end_date'],
        )


# https://docs.python.org/3/library/abc.html
# You can also register unrelated concrete classes (even built-in classes)
# and unrelated ABCs as “virtual subclasses” – these and their descendants
# will be considered subclasses of the registering ABC by the built-in
# issubclass() function, but the registering ABC won’t show up in their MRO
# (Method Resolution Order) nor will method implementations defined by the
# registering ABC be callable (not even via super())
DomainModel.register(Datathon)
