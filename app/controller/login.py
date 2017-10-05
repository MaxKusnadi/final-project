import requests
import logging

from flask_login import login_user

from app.models.user import User
from app.constants.ivle import (IVLE_URL, METRIC_URL,
                                NAME_URL, VALIDATE_URL,
                                API_KEY, EMAIL_URL)
from app import db, login_manager


@login_manager.user_loader
def load_user(metric):
    return User.query.filter(User.metric == metric).first()


class LoginController:

    def login(self, token):
        is_token_valid = self._validate_token(token)
        if is_token_valid:
            metric = self._get_metric(token)

            user = User.query.filter(User.metric == metric).first()
            if not user:
                name = self._get_name(token)
                email = self._get_email(token)
                user = User(metric, name, email)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            d = dict()
            d['name'] = user.name
            d['email'] = user.email
            d['metric'] = user.metric
            return d, 200
        return "Invalid Token"

    def _validate_token(self, token):
        validate_url = IVLE_URL + VALIDATE_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(validate_url, params=params).json()
        return resp['Success']

    def _get_metric(self, token):
        url = IVLE_URL + METRIC_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(url, params=params).text
        return resp

    def _get_name(self, token):
        url = IVLE_URL + NAME_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(url, params=params).text
        return resp

    def _get_email(self, token):
        url = IVLE_URL + EMAIL_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(url, params=params).text
        return resp
