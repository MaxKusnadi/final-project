import json

from flask import request, Response
from flask.views import MethodView
from flask_login import login_required, current_user

from app import app, socketio, logger
from app.constants.error import Error
from app.controller.attendance import AttendanceController
from app.controller.attendance_socket import on_connect


class AttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController(socketio)

    def post(self, session_id):
        logger.info("New POST /session/<string:session_id>/attendance request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("code"):
            return json.dumps(Error.CODE_NOT_FOUND)
        result = self.control.create_user_attendance(current_user, session_id, **data)
        return json.dumps(result)

    def patch(self, session_id):
        logger.info("New PATCH /session/<string:session_id>/attendance request")
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
        logger.info("New GET /session/<string:session_id>/attendance request")
        result = self.control.get_session_attendance(session_id, current_user)
        return json.dumps(result)


class MyAttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController(socketio)

    def get(self, session_id):
        logger.info("New GET /session/<string:session_id>/attendance/me request")
        result = self.control.get_my_session_attendance(session_id, current_user)
        return json.dumps(result)


class GroupAttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def get(self, course_id, group_id):
        logger.info("New GET /course/<string:course_id>/group/<int:group_id>/attendance request")
        result = self.control.get_group_attendance(current_user, course_id, group_id)
        return json.dumps(result)


class MyGroupAttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def get(self, course_id, group_id):
        logger.info("New GET /course/<string:course_id>/group/<int:group_id>/attendance request")
        result = self.control.get_my_group_attendance(current_user, course_id, group_id)
        return json.dumps(result)


class DownloadGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.control = AttendanceController()

    def get(self, course_id, group_id):
        logger.info("New GET /course/<string:course_id>/group/<int:group_id>/attendance request")
        result = self.control.download_group_attendance(current_user, course_id, group_id)
        if result['status'] == 200:
            return Response(
                result['result'],
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-disposition": "attachment; filename=group_{}_attendance.xls".format(group_id)})
        return json.dumps(result)


app.add_url_rule('/session/<int:session_id>/attendance', view_func=AttendanceView.as_view('attendance'))
app.add_url_rule('/session/<int:session_id>/attendance/me', view_func=MyAttendanceView.as_view('my_attendance'))
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>/attendance', view_func=GroupAttendanceView.as_view('group_attendance'))
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>/attendance/me', view_func=MyGroupAttendanceView.as_view('my_group_attendance'))
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>/attendance/download', view_func=DownloadGroupView.as_view('download_excel'))
socketio.on_event('connect', on_connect)
