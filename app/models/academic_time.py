from sqlalchemy import Column, String, Integer
from app import db


class AcademicTime(db.Model):
    __tablename__ = 'academictime'

    id = Column(Integer, primary_key=True)
    week_name = Column(String)
    even_odd_week = Column(String)
    acad_year = Column(String)
    semester = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)

    def __init__(self, week_name, even_odd_week, acad_year, semester, start_date, end_date):
        self.week_name = week_name
        self.even_odd_week = even_odd_week
        self.acad_year = acad_year
        self.semester = semester
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):  # pragma: no cover
        return "Week: {week_name} Acad_Year: {acad_year} Semester: {semester}".format(
            week_name=self.week_name, acad_year=self.acad_year, semester=self.semester
        )
