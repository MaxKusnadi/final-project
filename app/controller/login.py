from flask_login import login_user

from app.models.user import User
from app.controller.utils.checker import Checker
from app.controller.utils.ivle import IVLEApi
from app.controller.utils.initializer import Initializer
from app import db, login_manager, logger, cache


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


class LoginController:

    def __init__(self):
        self.initializer = Initializer()

    def login(self, token):
        # VALIDATE_TOKEN API is somehow broken. We bypass this for a while
        # logger.info("Validating token...")
        # is_token_valid, token = IVLEApi.validate_token(token)
        # if is_token_valid:
        profile = IVLEApi.get_profile(token)
        try:
            matric = profile['UserID']
        except:
            logger.error("Invalid token {}".format(token))
            d = dict()
            d['text'] = "Invalid Token"
            d['status'] = 301
            return d

        user = self._get_user(matric)
        if not user:
            logger.info("Creating user with UserID {}".format(matric))
            name = profile['Name']
            email = profile['Email']
            user = User(matric, name, email)
            db.session.add(user)
            db.session.commit()
        user.token = token
        login_user(user)
        if not user.is_data_pulled:
            self.initializer.initialize_user(user, token)
            user.is_data_pulled = True
        db.session.commit()
        d = dict()
        d['name'] = user.name
        d['email'] = user.email
        d['matric'] = user.matric
        d['status'] = 200
        return d

    def mock_login(self, **kwargs):
        matric = kwargs.get('matric')
        logger.info("Logging in for mocked user {}".format(matric))
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

    @cache.memoize()
    def _get_user(self, matric):
        return User.query.filter(User.matric == matric).first()

    @cache.memoize()
    def get_user_info(self, user):
        logger.info("Getting information for user {}".format(user.matric))
        d = dict()
        d['name'] = user.name
        d['email'] = user.email
        d['matric'] = user.matric
        d['status'] = 200
        return d
