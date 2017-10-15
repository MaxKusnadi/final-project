import logging
import json

from flask.views import MethodView
from flask import request
from flask_login import current_user, login_required

from app import app
from app.controller.user import UserController
from app.constants.error import Error


class UserView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def post(self):
        logging.info("New POST /mock/user request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("metric"):
            return json.dumps(Error.METRIC_NOT_FOUND)
        result = self.control.create_user(**data)
        return json.dumps(result)

    def get(self, metric_id):
        logging.info("New GET /mock/user request")
        if not metric_id:
            return json.dumps(Error.METRIC_NOT_FOUND)
        result = self.control.get_user(metric_id)
        return json.dumps(result)


class MyProfileView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logging.info("New GET /mock/me request")

        result = self.control.get_my_info(current_user)
        return json.dumps(result)


user_view = UserView.as_view('mock_user')
app.add_url_rule('/mock/user', view_func=user_view, methods=['POST'])
app.add_url_rule('/mock/user/<string:metric_id>', view_func=user_view, methods=['GET'])
app.add_url_rule('/mock/me', view_func=MyProfileView.as_view('mock_my_profile'))
