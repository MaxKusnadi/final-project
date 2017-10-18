import logging

from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db


class MockUserController:

    def create_user(self, **kwargs):
        logging.info("Creating a mocked user")
        name = kwargs.get('name', "")
        metric = kwargs.get("metric")
        email = kwargs.get('email', '')

        user = User.query.filter(User.metric == metric).first()
        error = Checker.check_user_exist(user)
        if error:
            return error

        user = User(metric, name, email)
        user.is_mocked = True
        db.session.add(user)
        db.session.commit()
        d = Utils.get_user_info(user)
        return d

    def get_user(self, matric_id):
        logging.info("Getting user {} info".format(matric_id))
        user = User.query.filter(User.metric == matric_id).first()
        error = Checker.check_mock_user(user, matric_id)
        if error:
            return error
        d = Utils.get_user_info(user)
        return d

    def get_my_info(self, user):
        logging.info("Getting user {} info".format(user.metric))
        d = Utils.get_user_info(user)
        return d
