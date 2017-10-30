import json

from flask.views import MethodView
from flask_login import current_user, login_required

from app import app, logger
from app.controller.user import UserController


class MyProfileView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logger.info("New GET /me request")

        result = self.control.get_my_info(current_user)
        return json.dumps(result)


class PullMyProfileView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logger.info("New GET /pull request")

        result = self.control.pull_my_info(current_user)
        return json.dumps(result)


class MarkMyProfileView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logger.info("New GET /mark-first-time request")

        result = self.control.mark_my_info(current_user)
        return json.dumps(result)


app.add_url_rule('/me', view_func=MyProfileView.as_view('my_profile'))
app.add_url_rule('/pull', view_func=PullMyProfileView.as_view('pull_profile'))
app.add_url_rule('/mark-first-time', view_func=MarkMyProfileView.as_view('mark_profile'))
