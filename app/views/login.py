import logging
import json

from flask.views import MethodView
from flask_login import login_required, logout_user, current_user
from flask import request, redirect

from app import app
from app.controller.login import LoginController
from app.constants.ivle import LOGIN_URL, LOGIN_REDIRECT_URL_DEV, LOGIN_REDIRECT_URL_LIVE


class LoginView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logging.info("New GET /login request")
        logging.info("CHECK THIS LOGIN {}".format(list(request.environ.keys())))
        if current_user.is_authenticated:
            result = self.control.get_user_info(current_user)
            return json.dumps(result)
        else:
            return redirect(LOGIN_URL)


class LoginStatusView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logging.info("New GET /login_status request")
        if current_user.is_authenticated:
            result = self.control.get_user_info(current_user)
            return json.dumps(result)
        else:
            logout_user()  # Destroy cookies
            return json.dumps({
                "text": "Not logged in",
                "status": 301}
            )


class LogoutView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logout_user()
        return redirect(LOGIN_REDIRECT_URL_DEV)


class IvleToken(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        token = request.args.get('token')
        logging.info("CHECK THIS TOKEN {}".format(request.environ.get("HTTP_ORIGIN")))
        self.control.login(token)
        return redirect(LOGIN_REDIRECT_URL_DEV)


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/ivle_token', view_func=IvleToken.as_view('ivle_token'))
app.add_url_rule('/login_status', view_func=LoginStatusView.as_view('login_status'))
