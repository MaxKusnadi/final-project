import logging
import json

from flask.views import MethodView
from flask import request

from app import app
from app.controller.login import LoginController
from app.constants.error import Error


class LoginView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def post(self):
        logging.info("New POST /mock/login request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("matric"):
            return json.dumps(Error.MATRIC_NOT_FOUND)
        result = self.control.mock_login(**data)
        return json.dumps(result)


app.add_url_rule('/mock/login', view_func=LoginView.as_view('mock_login'))
