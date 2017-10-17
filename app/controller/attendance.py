from flask_socketio import Namespace, emit, join_room
from time import time
from app.constants.time import COUNTDOWN_TIMEOUT

class AttendanceController(Namespace):

    def __init__(self, *args):
        super().__init__(*args)

    def on_connect(self):
        join_room('1')

    def on_start_count_down(self):
        current_time = time() + COUNTDOWN_TIMEOUT
        emit('count_down_received', current_time, room='1', broadcast=True)
