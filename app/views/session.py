import json

from flask.views import MethodView
from flask_login import login_required, current_user

from app import app, socketio, logger
from app.controller.session import SessionController


class SessionView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = SessionController()

    def get(self, session_id):
        logger.info("New GET /session request")
        if session_id is None:
            result = self.control.get_users_sessions(current_user)
        else:
            result = self.control.get_session_info(session_id, current_user)
        return json.dumps(result)


class SessionCodeView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = SessionController()

    def get(self, session_id):
        logger.info("New GET /session/<string:session_id>/code request")
        result = self.control.get_session_code(session_id, current_user)
        return json.dumps(result)


class StartSessionView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = SessionController(socketio)

    def get(self, session_id):
        logger.info("New GET /session/<string:session_id>/start request")
        result = self.control.start_session(session_id, current_user)
        return json.dumps(result)


session_view = SessionView.as_view('session')
app.add_url_rule('/session', defaults={'session_id': None}, view_func=session_view, methods=['GET'])
app.add_url_rule('/session/<int:session_id>', view_func=session_view, methods=['GET'])
app.add_url_rule('/session/<int:session_id>/code', view_func=SessionCodeView.as_view('session_code'))
app.add_url_rule('/session/<int:session_id>/start', view_func=StartSessionView.as_view('start_session'))
