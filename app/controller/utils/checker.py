from app.constants.error import Error
from app.controller.utils.utils import Utils


class Checker:

    @staticmethod
    def check_user_exist(user):
        if user:
            d = Utils.create_error_code(Error.USER_EXIST, user.metric)
            return d
        return None

    @staticmethod
    def check_mock_user(user, matric):
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, matric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, matric)
            return d
        return None
