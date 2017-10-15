import logging

from app.models.user import User
from app.controller.utils import Utils
from app.constants.error import Error
from app import db


class UserController:

    def create_user(self, **kwargs):
        logging.info("Creating a mocked user")
        name = kwargs.get('name', "")
        metric = kwargs.get("metric")
        email = kwargs.get('email', '')

        user = User.query.filter(User.metric == metric).first()
        if user:
            d = Utils.create_error_code(Error.USER_EXIST, metric)
            return d
        user = User(metric, name, email)
        user.is_mocked = True
        db.session.add(user)
        db.session.commit()
        d = self._get_user_info(user)
        return d

    def get_user(self, metric_id):
        logging.info("Getting user {} info".format(metric_id))
        user = User.query.filter(User.metric == metric_id).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, metric_id)
            return d
        d = self._get_user_info(user)
        return d

    def get_my_info(self, user):
        logging.info("Getting user {} info".format(user.metric))
        d = self._get_user_info(user)
        return d

    def _get_user_info(self, user):
        d = dict()
        d['name'] = user.name
        d['metric'] = user.metric
        d['email'] = user.email
        d['status'] = 200
        return d
