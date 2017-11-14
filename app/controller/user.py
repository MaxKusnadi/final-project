from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app.controller.utils.initializer import Initializer
from app import db, logger, cache


class UserController:

    def __init__(self):
        self.initializer = Initializer()

    @cache.memoize()
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
