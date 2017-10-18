import logging
import random

from datetime import datetime
from app.constants.time import TIMEZONE
from app.models.group import Group
from app.models.session import Session
from app.models.user import User
from app.controller.utils.utils import Utils
from app.constants.error import Error
from app import db


class MockSessionController:

    def create_session(self, **kwargs):
        logging.info("Creating a mocked session")
        group_id = kwargs.get('group_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        start_date = int(start_date) if start_date else None
        end_date = int(end_date) if end_date else None

        group = Group.query.filter(Group.id == group_id).first()
        if not group:
            d = Utils.create_error_code(Error.GROUP_WITH_ID_NOT_FOUND, group_id)
            return d
        if not group.is_mocked:
            d = Utils.create_error_code(Error.GROUP_NOT_MOCKED, group_id)
            return d
        session = Session(group, "9", start_date, end_date)
        session.is_mocked = True
        db.session.add(session)
        db.session.commit()
        d = Utils.get_session_info(session)
        d['status'] = 200
        return d

    def get_users_sessions(self, matric):
        logging.info("Getting all sessions for user {} this week".format(matric))
        user = User.query.filter(User.matric == matric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, matric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, matric)
            return d

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        week_info = Utils.get_week_name(now_epoch)
        week_name = week_info['week_name']

        groups_taken = user.groups
        groups_taught = user.groups_taught

        sessions_taken = []
        sessions_taught = []
        for group in groups_taken:
            sessions_taken.extend(group.sessions)
        for group in groups_taught:
            sessions_taught.extend(group.sessions)

        sessions_taken = list(filter(lambda x: x['week_name'] == week_name, sessions_taken))
        sessions_taught = list(filter(lambda x: x['week_name'] == week_name, sessions_taught))
        sessions_taken = list(map(lambda x: Utils.get_session_info(x), sessions_taken))
        sessions_taught = list(map(lambda x: Utils.get_session_info(x), sessions_taught))

        d = dict()
        d['session_taken'] = sessions_taken
        d['session_taught'] = sessions_taught
        d['status'] = 200
        return d

    def get_session_info(self, session_id, matric):
        logging.info("Getting session {} info for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        if not session:
            d = Utils.create_error_code(Error.SESSION_NOT_FOUND, session_id)
            return d
        if not session.is_mocked:
            d = Utils.create_error_code(Error.SESSION_NOT_MOCKED, session_id)
            return d
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

    def get_session_code(self, session_id, matric):
        logging.info("Getting session {} code for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        if not session:
            d = Utils.create_error_code(Error.SESSION_NOT_FOUND, session_id)
            return d
        if not session.is_mocked:
            d = Utils.create_error_code(Error.SESSION_NOT_MOCKED, session_id)
            return d

        user = User.query.filter(User.matric == matric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, matric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, matric)
            return d
        group = session.group
        if user not in group.staffs:
            d = Utils.create_error_code(Error.USER_NOT_AUTHORIZED, matric)
            return d
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

    def start_session(self, session_id, matric):
        logging.info("Getting session {} code for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        if not session:
            d = Utils.create_error_code(Error.SESSION_NOT_FOUND, session_id)
            return d
        if not session.is_mocked:
            d = Utils.create_error_code(Error.SESSION_NOT_MOCKED, session_id)
            return d

        user = User.query.filter(User.matric == matric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, matric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, matric)
            return d
        group = session.group
        if user not in group.staffs:
            d = Utils.create_error_code(Error.USER_NOT_AUTHORIZED, matric)
            return d

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        session.attendance_start_time = now_epoch
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['attendance_start_time'] = now_epoch
        d['status'] = 200
        return d

