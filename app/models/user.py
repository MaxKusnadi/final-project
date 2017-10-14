from flask_login import UserMixin
from sqlalchemy import Column, String, Integer
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    metric = Column(String, unique=True)
    name = Column(String)
    email = Column(String)
    token = Column(String)

    def __init__(self, metric, name, email=""):
        self.metric = metric
        self.name = name
        self.email = email
        self.token = ""

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):  # pragma: no cover
        return "Metric: {metric} - Name: {name} - Email: {email}".format(
            metric=self.metric, name=self.name, email=self.email
        )
