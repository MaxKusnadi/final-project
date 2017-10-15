from sqlalchemy import Column, String, Integer
from app import db


class WeekCode(db.Model):
    __tablename__ = 'weekcode'

    id = Column(Integer, primary_key=True)
    week_code = Column(Integer)
    description = Column(String)

    def __init__(self, week_code, description):
        self.week_code = week_code
        self.description = description

    def __repr__(self):  # pragma: no cover
        return "Week Code: {week_code} Description: {description}".format(
            week_code=self.week_code, description=self.description
        )
