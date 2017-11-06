import json

from flask.views import MethodView
from flask_login import login_required, logout_user, current_user
from flask import request, redirect

from app import app, logger
from app.controller.login import LoginController
from app.constants.ivle import LOGIN_URL, LOGIN_REDIRECT_URL_DEV, LOGIN_REDIRECT_URL_LIVE


class LoginView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logger.info("New GET /login request")
        logger.info("Request referer: {}".format(request.environ.get("HTTP_REFERER")))
        referer = request.environ.get("HTTP_REFERER")
        if current_user.is_authenticated:
            if referer and "https://nusattend.firebaseapp.com/" in referer:
                return redirect(LOGIN_REDIRECT_URL_LIVE)
            return redirect(LOGIN_REDIRECT_URL_DEV)
        else:
            return redirect(LOGIN_URL + "?referer={}".format(referer))


class LoginStatusView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logger.info("New GET /login_status request")
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
        referer = request.environ.get("HTTP_REFERER")
        if referer and "https://nusattend.firebaseapp.com/" in referer:
            return redirect(LOGIN_REDIRECT_URL_LIVE)
        return redirect(LOGIN_REDIRECT_URL_DEV)


class IvleToken(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        token = request.args.get('token')
        referer = request.args.get('referer')
        self.control.login(token)
        if referer and "https://nusattend.firebaseapp.com/" in referer:
                return redirect(LOGIN_REDIRECT_URL_LIVE)
        return redirect(LOGIN_REDIRECT_URL_DEV)


app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/ivle_token', view_func=IvleToken.as_view('ivle_token'))
app.add_url_rule('/login_status', view_func=LoginStatusView.as_view('login_status'))
