import logging
import json

from flask.views import MethodView
from flask_login import login_required, logout_user, current_user
from flask import request, redirect

from app import app
from app.controller.login import LoginController
from app.constants.ivle import LOGIN_URL, LOGIN_REDIRECT_URL


class LoginView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logging.info("New /login request")
        if current_user.is_authenticated:
            result = self.control.login_user(current_user)
            return json.dumps(result)
        else:
            return redirect(LOGIN_URL)


class LoginStatusView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logging.info("New /login_status request")
        if current_user.is_authenticated:
            result = self.control.login_user(current_user)
            return json.dumps(result)
        else:
            logout_user()  # Destroy cookies
            return "Not logged in"


class LogoutView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logout_user()
        return "Logged out"


class IvleToken(MethodView):

    def __init__(self):
        self.control = LoginController()

    def get(self):
        token = request.args.get('token')
        self.control.login(token)
        return redirect(LOGIN_REDIRECT_URL)  # TODO change localhost to different url according to env


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/ivle_token', view_func=IvleToken.as_view('ivle_token'))
app.add_url_rule('/login_status', view_func=LoginStatusView.as_view('login_status'))
