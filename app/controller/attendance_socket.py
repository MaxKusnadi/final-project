import logging

from datetime import datetime
from flask_socketio import Namespace, emit, join_room, disconnect
from flask_login import current_user

from app.constants.time import TIMEZONE
from app.controller.utils.utils import Utils


def on_connect():
    if current_user.is_authenticated:
        logging.info("User {} is connected".format(current_user.name))
        room_id = _get_room_id(current_user)
        if room_id:
            logging.info("{} join room {}".format(current_user.name, room_id))
            join_room(str(room_id))
            emit("count_down_received", data={"Hello": "hello"}, room=room_id)
        else:
            logging.info("Room id not found")
    else:
        logging.info("NOT AUTHENTICATED")
        disconnect()

def _get_room_id(user):
    now = datetime.now(TIMEZONE)
    now_epoch = int(now.timestamp())
    week_info = Utils.get_week_name(now_epoch)
    week_name = week_info['week_name']

    groups_taken = user.groups
    groups_taken = list(map(lambda x: x.group, groups_taken))
    groups_taught = user.groups_taught
    groups_taught = list(map(lambda x: x.group, groups_taught))

    all_sessions = []

    for group in groups_taken:
        all_sessions.extend(group.sessions)
    for group in groups_taught:
        all_sessions.extend(group.sessions)

    all_sessions = list(filter(lambda x: x.week_name == week_name, all_sessions))
    if len(all_sessions) == 0:
        return

    sorted_sessions = sorted(all_sessions, key=lambda x: x.start_date)
    room_id = sorted_sessions[0].id
    return room_id

#
# class AttendanceSocket(Namespace):
#
#     def __init__(self, *args):
#         super().__init__(*args)
#
#     def on_connect(self):
#         logging.info(current_user)
#         if current_user.is_authenticated:
#             logging.info("User {} is connected".format(current_user.name))
#             room_id = self._get_room_id(current_user)
#             if room_id:
#                 logging.info("{} join room {}".format(current_user.name, room_id))
#                 join_room(room_id)
#             else:
#                 logging.info("Room id not found")
#         else:
#             logging.info("NOT AUTHENTICATED")
#             disconnect()
#
#     def _get_room_id(self, user):
#         now = datetime.now(TIMEZONE)
#         now_epoch = int(now.timestamp())
#         week_info = Utils.get_week_name(now_epoch)
#         week_name = week_info['week_name']
#
#         groups_taken = user.groups
#         groups_taken = list(map(lambda x: x.group, groups_taken))
#         groups_taught = user.groups_taught
#         groups_taught = list(map(lambda x: x.group, groups_taught))
#
#         all_sessions = []
#
#         for group in groups_taken:
#             all_sessions.extend(group.sessions)
#         for group in groups_taught:
#             all_sessions.extend(group.sessions)
#
#         all_sessions = list(filter(lambda x: x.week_name == week_name, all_sessions))
#         if len(all_sessions) == 0:
#             return
#
#         sorted_sessions = sorted(all_sessions, key=lambda x: x.start_date)
#         room_id = sorted_sessions[0].id
#         return room_id
#
#     def start_count_down(self, count_down, session_id):
#         logging.info("Emmiting count down to room {}".format(session_id))
#         room_id = str(session_id)
#         emit('count_down_received', count_down, room=room_id)
#
#     def post_student_attendance(self, user, session_id):
#         logging.info("Emmitting attendance info for {}".format(user.info))
#         room_id = str(session_id)
#         emit("attendance_taken", Utils.get_user_info(user), room=room_id)
