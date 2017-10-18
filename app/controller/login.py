import logging

from flask_login import login_user

from app.models.user import User
from app.controller.utils.checker import Checker
from app.controller.utils.ivle import IVLEApi
from app import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


class LoginController:

    def login(self, token):
        logging.info("Validating token...")
        is_token_valid, token = IVLEApi.validate_token(token)
        if is_token_valid:
            profile = IVLEApi.get_profile(token)
            matric = profile['UserID']

            user = User.query.filter(User.matric == matric).first()
            if not user:
                logging.info("Creating user with UserID {}".format(matric))
                name = profile['Name']
                email = profile['Email']
                user = User(matric, name, email)
                db.session.add(user)
                db.session.commit()
            user.token = token
            db.session.commit()
            login_user(user)
            d = dict()
            d['name'] = user.name
            d['email'] = user.email
            d['matric'] = user.matric
            d['status'] = 200
            return d
        logging.error("Invalid token {}".format(token))
        d = dict()
        d['text'] = "Invalid Token"
        d['status'] = 301
        return d

    def mock_login(self, **kwargs):
        matric = kwargs.get('matric')
        logging.info("Logging in for mocked user {}".format(matric))
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error
        login_user(user)
        d = dict()
        d['name'] = user.name
        d['email'] = user.email
        d['matric'] = user.matric
        d['status'] = 200
        return d

    def get_user_info(self, user):
        logging.info("Getting information for user {}".format(user.matric))
        d = dict()
        d['name'] = user.name
        d['email'] = user.email
        d['matric'] = user.matric
        d['status'] = 200
        return d
