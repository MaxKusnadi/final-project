from flask_login import UserMixin
from sqlalchemy import Column, String
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    metric = Column(String, primary_key=True, unique=True)
    name = Column(String)
    email = Column(String)

    def __init__(self, metric, name, email):
        self.metric = metric
        self.name = name
        self.email = email

    def is_active(self):
        return True

    def get_id(self):
        return self.metric

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):  # pragma: no cover
        return "Metric: {metric} - Name: {name} - Email: {email}".format(
            metric= self.metric, name=self.name, email=self.email
        )
