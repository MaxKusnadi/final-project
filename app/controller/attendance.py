import logging

from app.models.attendance import Attendance
from app.models.group import Group
from app.models.session import Session
from app.models.course import Course
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db


class AttendanceController:

    def create_user_attendance(self, user, session_id, **kwargs):
        logging.info("Creating an attendance for {}".format(user.name))
        code = kwargs.get('code')

        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_student_group(user, group)
        if error:
            return error

        error = Checker.check_attendance_code(session, code)
        if error:
            return error

        attendance = Attendance.query.filter(Attendance.session_id == session_id,
                                             Attendance.user_id == user.id).first()
        if not attendance:
            attendance = Attendance(user, session, 1)
            db.session.add(attendance)
            db.session.commit()
        attendance.status = 1
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['status'] = 200
        return d

    def patch_user_attendance(self, user, session_id, **kwargs):
        logging.info("Patching an attendance by {}".format(user.name))
        status = kwargs.get("status")
        status = int(status)
        matric = kwargs.get("matric")
        remark = kwargs.get("remark", "")

        user_db = User.query.filter(User.matric == matric).first()
        error = Checker.check_user(user_db)
        if error:
            return error

        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_staff_group(user, group)
        if error:
            return error

        attendance = Attendance.query.filter(Attendance.session_id == session_id,
                                             Attendance.user_id == user_db.id).first()
        if not attendance:
            attendance = Attendance(user, session, status)
            db.session.add(attendance)
            db.session.commit()
        attendance.status = status
        attendance.remark = remark if remark else attendance.remark
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['status'] = 200
        return d

    def get_session_attendance(self, session_id, user):
        logging.info("Getting session {} attendance info for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error
        group = session.group
        error = Checker.check_is_user_staff_group(user, group)
        if error:
            return error

        total_attendance = group.students
        total_attendance = list(map(lambda x: x.user, total_attendance))
        attendance = self._get_attendance_helper(session, total_attendance)

        d = dict()
        d['attendance'] = attendance
        d['status'] = 200
        return d

    def get_group_attendance(self, user, course_code, group_name, group_type):
        logging.info("Getting group {}/{} attendance for {}".format(group_name, course_code, user.name))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_code, group_name, group_type)
        if error:
            return error

        sessions = group.sessions
        total_attendance = group.students
        total_attendance = list(map(lambda x: x.user, total_attendance))

        attendance = list(map(lambda x: {
            "week_name": x.week_name,
            "attendance": self._get_attendance_helper(x, total_attendance)
        }, sessions))
        d = dict()
        d['attendance'] = attendance
        d['status'] = 200
        return d

    def _get_attendance_helper(self, session, total_attendance):
        attendance = session.student
        attendance_user_matric = list(map(lambda x: x.user.matric, attendance))
        missing_student = list(filter(lambda x: x.matric not in attendance_user_matric, total_attendance))
        attendance = list(map(lambda x: Utils.get_attendance_info(x), attendance))
        missing_attendance = list(map(lambda x: Utils.get_missing_attendance_info(x), missing_student))
        attendance.extend(missing_attendance)
        return attendance