from datetime import datetime, timedelta
import jwt

from datacontest.shared.domain_model import DomainModel


class User:
    def __init__(self,
                 id,
                 username,
                 password,
                 email,
                 created_at=None,
                 is_admin=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.is_admin = is_admin

        if created_at is None:
            self.created_at = datetime.now()

        if is_admin is None:
            self.is_admin = False

        self.set_password(password)

    @classmethod
    def from_dict(cls, data):
        return User(
            id=data['id'],
            username=data['username'],
            password=data['password'],
            email=data['email'],
            created_at=data.get('created_at'),
            is_admin=data.get('is_admin'),
        )

    def set_password(self, password):
        from bcrypt import hashpw, gensalt
        self.hash = hashpw(password.encode('utf-8'), gensalt())

    def is_valid_password(self, password):
        from bcrypt import hashpw
        return hashpw(password.encode('utf-8'), self.hash) == self.hash




DomainModel.register(User)


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
