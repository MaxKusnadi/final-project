from app.constants.error import Error
from app.controller.utils.utils import Utils


class Checker:

    @staticmethod
    def check_user_exist(user):
        return Utils.create_error_code(Error.USER_EXIST, user.metric) if user else None

    @staticmethod
    def check_course_exist(course):
        return Utils.create_error_code(Error.COURSE_EXIST, course.course_code) if course else None

    @staticmethod
    def check_group_exist(group):
        return Utils.create_error_code(Error.GROUP_EXIST, group.group_name) if group else None

    @staticmethod
    def check_session_exist(session):
        return Utils.create_error_code(Error.SESSION_EXISTS, session.id) if session else None

    @staticmethod
    def check_mock_user(user, *args):
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, *args)
            return d
        return Utils.create_error_code(Error.USER_NOT_MOCKED, *args) if not user.is_mocked else None

    @staticmethod
    def check_mock_course(course, *args):
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, *args)
            return d
        return Utils.create_error_code(Error.COURSE_NOT_MOCKED, *args) if not course.is_mocked else None

    @staticmethod
    def check_course(course, *args):
        return Utils.create_error_code(Error.COURSE_NOT_FOUND, *args) if not course else None

    @staticmethod
    def check_mock_group(group, *args):
        if not group:
            d = Utils.create_error_code(Error.GROUP_NOT_FOUND, *args)
            return d
        return Utils.create_error_code(Error.GROUP_NOT_MOCKED, group.id) if not group.is_mocked else None

    @staticmethod
    def check_group(group, *args):
        return Utils.create_error_code(Error.GROUP_NOT_FOUND, *args) if not group else None

    @staticmethod
    def check_mock_group_id(group, *args):
        if not group:
            d = Utils.create_error_code(Error.GROUP_WITH_ID_NOT_FOUND, *args)
            return d
        return Utils.create_error_code(Error.GROUP_NOT_MOCKED, group.id) if not group.is_mocked else None

    @staticmethod
    def check_mock_session(session, *args):
        if not session:
            d = Utils.create_error_code(Error.SESSION_NOT_FOUND, *args)
            return d
        return Utils.create_error_code(Error.SESSION_NOT_MOCKED, session.id) if not session.is_mocked else None

    @staticmethod
    def check_session(session, *args):
        return Utils.create_error_code(Error.SESSION_NOT_FOUND, *args) if not session else None

    @staticmethod
    def check_user_in_group(user, group):
        return Utils.create_error_code(Error.USER_NOT_AUTHORIZED, user.matric) if user not in group.staffs else None
