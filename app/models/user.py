from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    matric = Column(String, unique=True)
    name = Column(String)
    email = Column(String)
    token = Column(String)
    is_data_pulled = Column(Boolean)
    is_mocked = Column(Boolean)

    def __init__(self, matric, name, email=""):
        self.matric = matric
        self.name = name
        self.email = email
        self.token = ""
        self.is_mocked = False
        self.is_data_pulled = False

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):  # pragma: no cover
        return "Matric: {matric} - Name: {name} - Email: {email}".format(
            matric=self.matric, name=self.name, email=self.email
        )
