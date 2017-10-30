from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app.controller.utils.initializer import Initializer
from app import db, logger


class UserController:

    def __init__(self):
        self.initializer = Initializer()

    def create_user(self, **kwargs):
        logger.info("Creating a mocked user")
        name = kwargs.get('name', "")
        matric = kwargs.get("matric")
        email = kwargs.get('email', '')

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_user_exist(user)
        if error:
            return error

        user = User(matric, name, email)
        user.is_mocked = True
        db.session.add(user)
        db.session.commit()
        d = Utils.get_user_info(user)
        return d

    def get_user(self, matric_id):
        logger.info("Getting user {} info".format(matric_id))
        user = User.query.filter(User.matric == matric_id).first()
        error = Checker.check_mock_user(user, matric_id)
        if error:
            return error
        d = Utils.get_user_info(user)
        return d

    def get_my_info(self, user):
        logger.info("Getting user {} info".format(user.matric))
        d = Utils.get_user_info(user)
        return d

    def pull_my_info(self, user):
        logger.info("Pulling user {} info from IVLE".format(user.name))
        self.initializer.initialize_user(user, user.token)
        d = dict()
        d['status'] = 200
        d['text'] = "Successful"
        return d

    def mark_my_info(self, user):
        logger.info("Marking user {} for first time usage".format(user.name))
        user.is_first_time = False
        db.session.commit()
        d = dict()
        d['status'] = 200
        d['text'] = "Successful"
        return d
