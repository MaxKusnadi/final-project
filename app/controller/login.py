import requests
import logging

from flask_login import login_user

from app.models.user import User
from app.constants.ivle import (IVLE_URL, VALIDATE_URL, API_KEY, PROFILE_URL)
from app import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


class LoginController:

    def login(self, token):
        logging.info("Validating token...")
        is_token_valid, token = self._validate_token(token)
        if is_token_valid:
            profile = self._get_profile(token)
            metric = profile['UserID']

            user = User.query.filter(User.metric == metric).first()
            if not user:
                logging.info("Creating user with UserID {}".format(metric))
                name = profile['Name']
                email = profile['Email']
                user = User(metric, name, email)
                db.session.add(user)
                db.session.commit()
            user.token = token
            db.session.commit()
            login_user(user)
            d = dict()
            d['name'] = user.name
            d['email'] = user.email
            d['metric'] = user.metric
            d['status'] = 200
            return d
        logging.error("Invalid token {}".format(token))
        d = dict()
        d['text'] = "Invalid Token"
        d['status'] = 301
        return d

    def get_user_info(self, user):
        logging.info("Getting information for user {}".format(user.metric))
        d = dict()
        d['name'] = user.name
        d['email'] = user.email
        d['metric'] = user.metric
        d['status'] = 200
        return d

    def _validate_token(self, token):
        validate_url = IVLE_URL + VALIDATE_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(validate_url, params=params).json()
        return resp['Success'], resp['Token']

    def _get_profile(self, token):
        url = IVLE_URL + PROFILE_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token
        }
        resp = requests.get(url, params=params).json()
        logging.info(resp)
        return resp['Results'][0]
