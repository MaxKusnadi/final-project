import logging
import random

from datetime import datetime, timedelta
from app.constants.time import TIMEZONE
from app.models.group import Group
from app.models.session import Session
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db


# class SessionController:
#     # INPUT: a group as outputted from get_groups, semester_start_date in epoch as stored in DB, semester (int)
#     # OUTPUT: a list of sessions, a session is a dictionary with keys: week_name, start_date, end_date
#     def generate_sessions(group, semester_start_date, semester):
#         first_monday = get_first_week_monday(datetime.fromtimestamp(semester_start_date), semester)
#         start_time, end_time, day_code, week_code = group['start_time'], group['end_time'], group['day_code'], group[
#             'week_code']
#         start_time_hours, start_time_minutes = int(start_time[:2]), int(start_time[2:])
#         end_time_hours, end_time_minutes = int(end_time[:2]), int(end_time[2:])
#         week_string = get_week_code_description(week_code)
#         week_deltas = convert_week_code_description_to_week_name(week_string)
#         days = map(lambda x: (x, first_monday + timedelta(days=day_code - 1) + timedelta(weeks=x - 1)), week_deltas)
#         return list(map(lambda x: {
#             'week_name': str(x[0]),
#             'start_date': int((x[1] + timedelta(hours=start_time_hours, minutes=start_time_minutes)).timestamp()),
#             'end_date': int((x[1] + timedelta(hours=end_time_hours, minutes=end_time_minutes)).timestamp())
#         }, days))
#
#     # Helper function of generate_sessions
#     def convert_week_code_description_to_week_name(week_code):
#         if week_code == 'EVERY WEEK':
#             return [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14]
#         elif week_code == 'ODD WEEK':
#             return [1, 3, 5, 8, 10, 12]
#         elif week_code == 'EVEN WEEK':
#             return [2, 4, 6, 9, 11, 13]
#         elif week_code == 'ORIENTATION WEEK':
#             return []  # dont care about orientatation week?
#         else:
#             return list(map(lambda x: (x + 1) if x > 6 else x, map(int, week_code.split(','))))
#
#     # Helper function of generate_sessions
#     def get_first_week_monday(semester_start_date, semester):
#         if semester == 1:
#             return semester_start_date + timedelta(days=7)
#         else:
#             return semester_start_date
#
#     ################ CODE NOT NEEDED, get_week_code_description need to be rewrite for actual production code ###################
#     def get_week_codes():
#         param = {
#             "APIKey": API_KEY
#         }
#         service = "CodeTable_WeekTypes"
#         url = IVLE_URL + service
#         resp = requests.get(url, params=param)
#         results = resp.json()['Results']
#         # print(list(filter(lambda x: not re.match('^[0-9]+(?:,[0-9]+)*$', x['Description']), results)))
#         return dict(list(map(lambda x: [int(x['WeekCode']), x['Description']], results)))
#
#     week_codes_map = get_week_codes()
#
#     def get_week_code_description(code):
#         return week_codes_map[code]
#         #################


class MockSessionController:

    def create_session(self, **kwargs):
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

    def get_users_sessions(self, matric):
        logging.info("Getting all sessions for user {} this week".format(matric))
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

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

    def get_session_code(self, session_id, matric):
        logging.info("Getting session {} code for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_mock_session(session, session_id)
        if error:
            return error

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
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

    def start_session(self, session_id, matric):
        logging.info("Getting session {} code for {}".format(session_id, matric))
        session = Session.query.filter(Session.id == session_id).first()
        error = Checker.check_mock_session(session, session_id)
        if error:
            return error

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        group = session.group
        error = Checker.check_user_in_group(user, group)
        if error:
            return error

        now = datetime.now(TIMEZONE)
        now_epoch = int(now.timestamp())
        session.attendance_start_time = now_epoch
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        d['attendance_start_time'] = now_epoch
        d['status'] = 200
        return d

