import logging
import random

from datetime import datetime, timedelta
from app.constants.time import TIMEZONE, COUNTDOWN_TIMEOUT
from app.models.group import Group
from app.models.session import Session
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app.controller.attendance_socket import AttendanceSocket
from app import db


class SessionController:

    def __init__(self):
        self.socket = AttendanceSocket()

    def create_mock_session(self, **kwargs):
        logging.info("Creating a mocked session")
        group_id = kwargs.get('group_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        start_date = int(start_date) if start_date else None
        end_date = int(end_date) if end_date else None

        group = Group.query.filter(Group.id == group_id).first()
        error = Checker.check_mock_group_id(group, group_id)
        if error:
            return error
        session = Session.query.filter(Session.group_id == group.id,
                                       Session.start_date == start_date,
                                       Session.end_date == end_date).first()
        error = Checker.check_session_exist(session)
        if error:
            return error
        session = Session(group, "9", start_date, end_date)
        session.is_mocked = True
        db.session.add(session)
        db.session.commit()
        d = Utils.get_session_info(session)
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

        code = random.randint(0, 1000000)
        code = str(code).zfill(6)
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
        logging.info("Starting session {} attendance for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_user_in_group(user, group)
        if error:
            return error

        closed_time = datetime.now(TIMEZONE) + timedelta(seconds=COUNTDOWN_TIMEOUT)
        now_epoch = int(closed_time.timestamp())

        error = Checker.check_is_session_open(session, now_epoch, session_id)
        if error:
            return error

        session.attendance_closed_time = now_epoch
        db.session.commit()

        self.socket.start_count_down(now_epoch, session_id)

        d = dict()
        d['text'] = "Success"
        d['attendance_closed_time'] = now_epoch
        d['status'] = 200
        return d

    # def stop_session(self, session_id, user):
    #     logging.info("Stopping session {} attendance for {}".format(session_id, user.name))
    #     session = Session.query.filter(Session.id == session_id).first()
    #     error = Checker.check_session(session, session_id)
    #     if error:
    #         return error
    #
    #     group = session.group
    #     error = Checker.check_user_in_group(user, group)
    #     if error:
    #         return error
    #
    #     session.is_open = True
    #     db.session.commit()
    #     d = dict()
    #     d['text'] = "Success"
    #     d['status'] = 200
    #     return d
