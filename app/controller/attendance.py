from datetime import datetime

from app.constants.time import TIMEZONE
from app.models.attendance import Attendance
from app.models.group import Group
from app.models.session import Session
from app.models.course import Course
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db, logger


class AttendanceController:

    def __init__(self, socket=None):
        self.socket = socket

    def create_user_attendance(self, user, session_id, **kwargs):
        logger.info("Creating an attendance for {}".format(user.name))
        code = kwargs.get('code')
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_student_group(user, group)
        if error:
            return error

        now = datetime.now(TIMEZONE).timestamp()

        error = Checker.check_attendance_code(session, now, code)
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

        # Emitting through socketio
        room_id = str(session_id)
        if self.socket:
            self.socket.emit("attendance_taken", Utils.get_user_info(user), room=room_id)

        d = dict()
        d['text'] = "Success"
        d['status'] = 200
        return d

    def patch_user_attendance(self, user, session_id, **kwargs):
        logger.info("Patching an attendance by {}".format(user.name))
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
        logger.info("Getting session {} attendance info for {}".format(session_id, user.name))
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

    def get_my_session_attendance(self, session_id, user):
        logger.info("Getting session {} attendance info for myself {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error
        group = session.group
        error = Checker.check_is_user_student_group(user, group)
        if error:
            return error

        attendance = Attendance.query.filter(Attendance.session_id == session.id,
                                             Attendance.user_id == user.id).first()
        status = attendance.status if attendance else 0

        d = dict()
        d['attendance'] = status
        d['status'] = 200
        return d

    def get_group_attendance(self, user, course_id, group_id):
        logger.info("Getting group {}/{} attendance for {}".format(group_id, course_id, user.name))
        course = Course.query.filter(Course.id == course_id).first()
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = Group.query.filter(Group.id == group_id,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error
        error = Checker.check_is_user_staff_group(user, group)
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

    def get_my_group_attendance(self, user, course_id, group_id):
        logger.info("Getting group {}/{} attendance for myself {}".format(group_id, course_id, user.name))
        course = Course.query.filter(Course.id == course_id).first()
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = Group.query.filter(Group.id == group_id,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error
        error = Checker.check_is_user_student_group(user, group)
        if error:
            return error

        sessions = group.sessions
        all_attendance = []

        for session in sessions:
            attendance = Attendance.query.filter(Attendance.session_id == session.id,
                                                 Attendance.user_id == user.id).first()
            status = attendance.status if attendance else 0
            all_attendance.append({
                "week_name": session.week_name,
                "attendance": status
            })

        d = dict()
        d['attendance'] = all_attendance
        d['status'] = 200
        return d

    def download_group_attendance(self, user, course_id, group_id):
        logger.info("Downloading group {}/{} attendance for myself {}".format(group_id, course_id, user.name))
        course = Course.query.filter(Course.id == course_id).first()
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = Group.query.filter(Group.id == group_id,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error
        error = Checker.check_is_user_staff_group(user, group)
        if error:
            return error

        sessions = group.sessions
        total_attendance = group.students
        total_attendance = list(map(lambda x: x.user, total_attendance))

        attendance = list(map(lambda x: {
            "week_name": x.week_name,
            "attendance": self._get_attendance_helper(x, total_attendance)
        }, sessions))

        # Creating excel
        file_name = "group_{}_attendance.xls".format(group_id)
        ans = []
        HEADER = ['NAME', 'MATRIC_NUMBER']
        total_weeks = len(attendance)
        for att in attendance:
            HEADER.append("WEEK_{}".format(att['week_name']))
        HEADER.append("TOTAL")
        ans.append(HEADER)

        # Filling in row by row
        for student in total_attendance:
            ROW = list()
            ROW.append("{}".format(student.name))
            ROW.append("{}".format(student.matric))
            count = 0
            for att in attendance:
                status = list(filter(lambda x: x['name'] == student.name, att['attendance']))[0]['status']
                count += status
                ROW.append("{}".format(status))
            ROW.append("{}/{}".format(count, total_weeks))
            ans.append(ROW)

        d = dict()
        d['filename'] = file_name
        d['result'] = ans
        d['status'] = 200
        return d

    def _get_attendance_helper(self, session, total_attendance):
        attendance = session.students
        attendance_user_matric = list(map(lambda x: x.user.matric, attendance))
        missing_student = list(filter(lambda x: x.matric not in attendance_user_matric, total_attendance))
        attendance = list(map(lambda x: Utils.get_attendance_info(x), attendance))
        missing_attendance = list(map(lambda x: Utils.get_missing_attendance_info(x), missing_student))
        attendance.extend(missing_attendance)
        return attendance
