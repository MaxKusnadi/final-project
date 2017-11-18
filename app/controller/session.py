import random

from datetime import datetime, timedelta
from app.constants.time import TIMEZONE, COUNTDOWN_TIMEOUT
from app.constants.encryption import CIPHER
from app.models.session import Session
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db, logger, cache


class SessionController:

    def __init__(self, socket=None):
        self.cipher = CIPHER
        self.socket = socket

    @cache.memoize(60)
    def get_users_sessions(self, user):
        logger.info("Getting closest for user {} this week".format(user.name))

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        week_info = Utils.get_week_name(now_epoch)
        week_name = week_info['week_name']

        groups = list()
        groups_taken = user.groups
        groups_taken = list(map(lambda x: x.group, groups_taken))
        groups.extend(groups_taken)
        groups_taught = user.groups_taught
        groups_taught = list(map(lambda x: x.group, groups_taught))
        groups.extend(groups_taught)

        sessions = list()
        for group in groups:
            sessions.extend(group.sessions)

        # Filter by week
        first_sessions = list(filter(lambda x: x.week_name == week_name, sessions))
        # Filter by time
        first_sessions = list(filter(lambda x: now_epoch <= x.end_date, first_sessions))

        # Check if it exists if not get the next week one
        if not first_sessions:
            try:
                week_name = str(int(week_name) + 1)
            exception:
                return {}
            first_sessions = list(filter(lambda x: x.week_name == week_name, sessions))
            # Filter by time
            first_sessions = list(filter(lambda x: now_epoch <= x.end_date, first_sessions))

        # Check if it exists. if not return empty
        if not first_sessions:
            return {}

        first_sessions = sorted(first_sessions, key=lambda x: x.start_date)
        closest_session = first_sessions[0]
        session_info = Utils.get_session_info(closest_session)
        session_info['session_type'] = "student" if closest_session.group in groups_taken else "staff"
        session_info['status'] = 200
        session_info['week_name'] = week_name
        return session_info

    @cache.memoize()
    def get_session_info(self, session_id, user):
        logger.info("Getting session {} info for {}".format(session_id, user.name))
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

    def get_session_code(self, session_id, user):
        logger.info("Getting session {} code for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_staff_group(user, group)
        if error:
            return error

        now_epoch = datetime.now(TIMEZONE)
        now_epoch = int(now_epoch.timestamp())

        error = Checker.check_is_session_open(session, now_epoch, session_id)
        if error:
            code = session.code
        else:
            code = random.randint(0, 1000000)
            code = str(code).zfill(6)
            session.code = code
            db.session.commit()

        d = dict()
        d['status'] = 200
        qr_code = self.cipher.encrypt(str.encode(code)).decode()
        d['code'] = code
        d['qr_code'] = qr_code
        return d

    def start_session(self, session_id, user):
        logger.info("Starting session {} attendance for {}".format(session_id, user.name))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_session(session, session_id)
        if error:
            return error

        group = session.group
        error = Checker.check_is_user_staff_group(user, group)
        if error:
            return error

        closed_time = datetime.now(TIMEZONE) + timedelta(seconds=COUNTDOWN_TIMEOUT)
        closed_time = int(closed_time.timestamp())
        now_epoch = datetime.now(TIMEZONE)
        now_epoch = int(now_epoch.timestamp())

        error = Checker.check_is_session_open(session, now_epoch, session_id)
        if error:
            d = dict()
            d['text'] = "Success"
            d['attendance_closed_time'] = session.attendance_closed_time
            d['status'] = 200
            return d

        session.attendance_closed_time = closed_time
        db.session.commit()

        # Emitting through socketio
        room_id = str(session_id)
        if self.socket:
            self.socket.emit('count_down_received', closed_time, room=room_id)

        d = dict()
        d['text'] = "Success"
        d['attendance_closed_time'] = closed_time
        d['status'] = 200
        return d
