from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app import db


class Group(db.Model):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("Course", backref="groups")

    course_name = Column(String)
    group_name = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)
    day_code = Column(Integer)
    week_code = Column(Integer)
    venue = Column(String)
    group_type = Column(String)
    is_mocked = Column(Boolean)

    def __init__(self, course, group_name, start_time,
                 end_time, day_code, week_code, venue, group_type):
        self.course = course
        self.course_id = course.id
        self.course_name = course.course_name
        self.group_name = group_name
        self.start_time = start_time
        self.end_time = end_time
        self.day_code = day_code
        self.week_code = week_code
        self.venue = venue
        self.group_type = group_type
        self.is_mocked = False


    def __repr__(self):
        return "{course_name} {group_type} {group_name} | Day: {day_code} Week: {week_code} Venue: {venue}".format(
            course_name=self.course_name, group_type=self.group_type, group_name=self.group_name,
            day_code=self.day_code, week_code=self.week_code, venue=self.venue
        )


class GroupStudent(db.Model):
    __tablename__ = 'groupStudent'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)

    user = relationship("User", backref="groups")
    group = relationship("Group", backref="students")

    def __init__(self, user, group):
        self.user = user
        self.group = group
        self.user_id = user.id
        self.group_id = group.id

    def __repr__(self):
        return "<STUDENT> User: {user} - Group: {group_id}".format(user=self.user.metric, group_id=self.group_id)


class GroupStaff(db.Model):
    __tablename__ = 'groupStaff'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)

    user = relationship("User", backref="groups_taught")
    group = relationship("Group", backref="staffs")

    def __init__(self, user, group):
        self.user = user
        self.group = group
        self.user_id = user.id
        self.group_id = group.id

    def __repr__(self):
        return "<STAFF> User: {user} - Group: {group_id}".format(user=self.user.metric, group_id=self.group_id)
