import logging
import random

from datetime import datetime
from app.constants.time import TIMEZONE
from app.models.attendance import Attendance
from app.models.group import Group
from app.models.session import Session
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
        matric = kwargs.get("matric")
        remark = kwargs.get("remark", "")

        user_db = User.query.filter(User.matric == matric).first()
        # error = Checker.check_user(user_db)
        # if error:
        #     return error

        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_staff_group(user, group)
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


    def get_mock_users_sessions(self, matric):
        logging.info("Getting all mock sessions for user {} this week".format(matric))
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        return self.get_users_sessions(user)

    def get_users_sessions(self, user):
        logging.info("Getting all sessions for user {} this week".format(user.name))

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        week_info = Utils.get_week_name(now_epoch)
        week_name = week_info['week_name']

        groups_taken = user.groups
        groups_taken = list(map(lambda x: x.group, groups_taken))
        groups_taught = user.groups_taught
        groups_taught = list(map(lambda x: x.group, groups_taught))

        sessions_taken = []
        sessions_taught = []
        for group in groups_taken:
            sessions_taken.extend(group.sessions)
        for group in groups_taught:
            sessions_taught.extend(group.sessions)

        sessions_taken = list(filter(lambda x: x.week_name == week_name, sessions_taken))
        sessions_taught = list(filter(lambda x: x.week_name == week_name, sessions_taught))
        sessions_taken = list(map(lambda x: Utils.get_session_info(x), sessions_taken))
        sessions_taught = list(map(lambda x: Utils.get_session_info(x), sessions_taught))

        d = dict()
        d['session_taken'] = sessions_taken
        d['session_taught'] = sessions_taught
        d['status'] = 200
        return d

    def get_mock_session_info(self, session_id, matric):
        logging.info("Getting session {} info for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_mock_session(session, session_id)
        if error:
            return error
        d = Utils.get_session_info(session)
        d['status'] = 200
        group = session.group
        user = User.query.filter(User.matric == matric).first()
        if user:
            if user in group.staffs:
                attendance = session.students
                attendance = list(map(lambda x: Utils.get_attendance_info(x), attendance))
                d['attendance'] = attendance
        return d

    def get_session_info(self, session_id, user):
        logging.info("Getting session {} info for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error
        d = Utils.get_session_info(session)
        d['status'] = 200
        group = session.group

        if user in group.staffs:
            attendance = session.students
            attendance = list(map(lambda x: Utils.get_attendance_info(x), attendance))
            d['attendance'] = attendance
        return d

    def get_mock_session_code(self, session_id, matric):
        logging.info("Getting mock session {} code for {}".format(session_id, matric))

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        return self.get_session_code(session_id, user)

    def get_session_code(self, session_id, user):
        logging.info("Getting session {} code for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_user_in_group(user, group)
        if error:
            return error

        d = dict()
        d['status'] = 200
        if session.code:
            d['code'] = session.code
            return d

        code = random.randint(0, 10000)
        code = str(code).zfill(4)
        session.code = code
        db.session.commit()
        d['code'] = code
        return d

    def start_mock_session(self, session_id, matric):
        logging.info("Stating mock session {} attendance for {}".format(session_id, matric))

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error
        return self.start_session(session_id, user)

    def start_session(self, session_id, user):
        logging.info("Stating session {} attendance for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_user_in_group(user, group)
        if error:
            return error

        error = Checker.check_is_session_open(session, session_id)
        if error:
            return error

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        session.attendance_start_time = now_epoch
        session.is_open = True
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['attendance_start_time'] = now_epoch
        d['status'] = 200
        return d

    def stop_session(self, session_id, user):
        logging.info("Stating session {} attendance for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_user_in_group(user, group)
        if error:
            return error

        session.is_open = True
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['status'] = 200
        return d
