from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app import db


class Session(db.Model):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship("Group", backref="sessions")

    week_name = Column(String)
    start_date = Column(Integer)
    end_date = Column(Integer)
    attendance_closed_time = Column(Integer)
    code = Column(String)
    is_mocked = Column(Boolean)

    def __init__(self, group, week_name, start_date, end_date):
        self.group = group
        self.group_id = group.id
        self.week_name = week_name
        self.start_date = start_date
        self.end_date = end_date
        self.attendance_closed_time = None
        self.code = None
        self.is_mocked = False

    def __repr__(self):
        return "Session for course {course} for week {week} at {start_date} to {end_date}".format(
            course=self.group.course.course_name, week=self.week_name, start_date=self.start_date, end_date=self.end_date
        )
