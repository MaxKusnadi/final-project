from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app import db


class Course(db.Model):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    creator_user_id = Column(String)
    creator_name = Column(String)
    course_id = Column(String)
    course_code = Column(String)
    course_name = Column(String)
    acad_year = Column(String)
    semester = Column(Integer)
    is_mocked = Column(Boolean)

    def __init__(self, creator_user_id, creator_name,
                 course_id, course_code, course_name,
                 acad_year, semester):
        self.creator_user_id = creator_user_id
        self.creator_name = creator_name
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.acad_year = acad_year
        self.semester = semester
        self.is_mocked = False

    def __repr__(self):
        return "{course_code}: {course_name} {acad_year}/{semester} by {creator_name}".format(
            course_code=self.course_code, course_name=self.course_name, acad_year=self.acad_year,
            semester=self.semester, creator_name=self.creator_name
        )


class CourseStudent(db.Model):
    __tablename__ = 'courseStudent'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    user = relationship("User", backref="courses_taken")
    course = relationship("Course", backref="students")

    def __init__(self, user, course):
        self.user = user
        self.course = course
        self.user_id = user.id
        self.course_id = course.id

    def __repr__(self):
        return "<STUDENT> User: {user} - Course: {course}".format(user=self.user.metric, course=self.course_id)


class CourseStaff(db.Model):
    __tablename__ = 'courseStaff'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    user = relationship("User", backref="courses_taught")
    course = relationship("Course", backref="staffs")

    def __init__(self, user, course):
        self.user = user
        self.course = course
        self.user_id = user.id
        self.course_id = course.id

    def __repr__(self):
        return "<STAFF> User: {user} - Course: {course}".format(user=self.user.metric, course=self.course_id)
