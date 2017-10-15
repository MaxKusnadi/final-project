from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Attendance(db.Model):
    __tablename__ = 'attendance'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), primary_key=True)
    user = relationship("User", backref="attendances")
    session = relationship("Session", backref="students")

    status = Column(Integer)
    remark = Column(String)

    def __init__(self, user, session, status, remark=""):
        self.user = user
        self.session = session
        self.user_id = user.id
        self.session_id = session.id
        self.status = status
        self.remark = remark

    def __repr__(self):
        return "Session: {session_id} | Student: {student_name} | Week: {week_name} | Status: {status}".format(
            session_id=self.session_id, student_name=self.user.name,
            week_name=self.session.week_name, status=self.status
        )
