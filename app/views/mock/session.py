import logging
import json

from flask.views import MethodView
from flask import request

from app import app
from app.controller.session import MockSessionController
from app.constants.error import Error


class SessionView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockSessionController()

    def post(self):
        logging.info("New POST /mock/session request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("group_id"):
            return json.dumps(Error.GROUP_ID_NOT_FOUND)
        if not data.get("start_date"):
            return json.dumps(Error.START_DATE_NOT_FOUND)
        if not data.get("end_date"):
            return json.dumps(Error.END_DATE_NOT_FOUND)
        result = self.control.create_session(**data)
        return json.dumps(result)

    def get(self, session_id):
        logging.info("New GET /mock/group request")
        metric = request.args.get('metric')
        if not metric:
            return json.dumps(Error.METRIC_NOT_FOUND)
        if session_id is None:
            result = self.control.get_users_sessions(metric)
        else:
            result = self.control.get_session_info(session_id, metric)
        return json.dumps(result)


class SessionCodeView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockSessionController()

    def get(self, session_id):
        logging.info("New GET /mock/session/<string:session_id>/code request")
        metric = request.args.get('metric')
        if not metric:
            return json.dumps(Error.METRIC_NOT_FOUND)
        if session_id is None:
            result = self.control.get_users_sessions(metric)
        else:
            result = self.control.get_session_code(session_id, metric)
        return json.dumps(result)


class StartSessionView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockSessionController()

    def get(self, session_id):
        logging.info("New GET /mock/session/<string:session_id>/start request")
        metric = request.args.get('metric')
        if not metric:
            return json.dumps(Error.METRIC_NOT_FOUND)
        if session_id is None:
            result = self.control.get_users_sessions(metric)
        else:
            result = self.control.start_session(session_id, metric)
        return json.dumps(result)


session_view = SessionView.as_view('mock_session')
app.add_url_rule('/mock/session', view_func=session_view, methods=['POST'])
app.add_url_rule('/mock/session', defaults={'session_id': None}, view_func=session_view, methods=['GET'])
app.add_url_rule('/mock/session/<string:session_id>', view_func=session_view, methods=['GET'])
app.add_url_rule('/mock/session/<string:session_id>/code', view_func=SessionCodeView.as_view('mock_session_code'))
app.add_url_rule('/mock/session/<string:session_id>/start', view_func=StartSessionView.as_view('mock_start_session'))
