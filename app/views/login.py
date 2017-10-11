import logging
import json

from flask.views import MethodView
from flask_login import login_required, logout_user
from flask import request, render_template, redirect, url_for

from app import app
from app.controller.login import LoginController


class LoginView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logging.info("New /login request")
        token = request.args.get('token')
        if token:
            result, status = self.control.login(token)
        else:
            return 'INVALID TOKEN'
        # return json.dumps(token), status
        return redirect(url_for('index'))


class LogoutView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = LoginController()

    def get(self):
        logout_user()
        # return "Logged Out"
        return redirect(url_for('index'))

class IndexView(MethodView):

    def get(self):
        return render_template('index.html')


class IvleView(MethodView):

    def get(self):
        return redirect("https://ivle.nus.edu.sg/api/login/?apikey=bAbUg4vhpnzADp7DO9GU0&url=http://localhost:3040/ivle_token")


class IvleToken(MethodView):

    def get(self):
        token = request.args.get('token')
        return redirect(url_for('login', token=token))

app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/login_ivle', view_func=IvleView.as_view('login_ivle'))
app.add_url_rule('/ivle_token', view_func=IvleToken.as_view('ivle_token'))
