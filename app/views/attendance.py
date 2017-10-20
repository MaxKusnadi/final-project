import logging
import json

from flask import request
from flask.views import MethodView
from flask_login import login_required, current_user

from app import app, socketio
from app.constants.error import Error
from app.controller.attendance import AttendanceController


class AttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def post(self, session_id):
        logging.info("New POST /session/<string:session_id>/attendance request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("code"):
            return json.dumps(Error.CODE_NOT_FOUND)
        result = self.control.create_user_attendance(current_user, session_id, **data)
        return json.dumps(result)

    def patch(self, session_id):
        logging.info("New PATCH /session/<string:session_id>/attendance request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("status"):
            return json.dumps(Error.CODE_NOT_FOUND)
        if not data.get("matric"):
            return json.dumps(Error.CODE_NOT_FOUND)
        result = self.control.patch_user_attendance(current_user, session_id, **data)
        return json.dumps(result)

    def get(self, session_id):
        logging.info("New GET /session/<string:session_id>/attendance request")
        result = self.control.get_session_attendance(session_id, current_user)
        return json.dumps(result)


class GroupAttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/group/attendance request")
        group_name = request.args.get('group_name')
        group_type = request.args.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
        result = self.control.get_group_attendance(current_user, course_code, group_name, group_type)
        return json.dumps(result)


app.add_url_rule('/session/<string:session_id>/attendance', view_func=AttendanceView.as_view('attendance'))
app.add_url_rule('/course/<string:course_code>/group/attendance', view_func=GroupAttendanceView.as_view('group_attendance'))
socketio.on_namespace(AttendanceController('/'))
