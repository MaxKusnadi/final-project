import logging
import json

from flask.views import MethodView
from flask_login import current_user, login_required

from app import app
from app.controller.user import UserController


class MyProfileView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logging.info("New GET /me request")

        result = self.control.get_my_info(current_user)
        return json.dumps(result)


app.add_url_rule('/me', view_func=MyProfileView.as_view('my_profile'))
