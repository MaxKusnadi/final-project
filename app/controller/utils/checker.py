from app.constants.error import Error
from app.controller.utils.utils import Utils


class Checker:

    @staticmethod
    def check_is_user_student_group(user, group):
        group_students = group.students
        found = list(filter(lambda x: x.user_id == user.id, group_students))
        return Utils.create_error_code(Error.USER_IS_NOT_STUDENT_GROUP,
                                       user.matric,
                                       group.group_name) if len(found) == 0 else None

    @staticmethod
    def check_is_user_staff_group(user, group):
        group_staffs = group.staffs
        found = list(filter(lambda x: x.user_id == user.id, group_staffs))
        return Utils.create_error_code(Error.USER_IS_NOT_STAFF_GROUP, user.matric,
                                       group.group_name) if len(found) == 0 else None

    @staticmethod
    def check_is_user_staff_course(user, course):
        course_staff = course.staffs
        found = list(filter(lambda x: x.user_id == user.id, course_staff))
        return Utils.create_error_code(Error.USER_IS_NOT_STAFF_COURSE,
                                       user.matric,
                                       course.course_code) if len(found) == 0 else None

    @staticmethod
    def check_attendance_code(session, now, code):
        if now > session.attendance_closed_time:
            return Utils.create_error_code(Error.SESSION_IS_CLOSED, session.id)
        return Utils.create_error_code(Error.CODE_IS_WRONG) if session.code != code else None

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
    def check_user(user, *args):
        return Utils.create_error_code(Error.USER_NOT_FOUND, *args) if not user else None

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
    def check_is_session_open(session, time_now, *args):
        return Utils.create_error_code(Error.SESSION_IS_OPEN, *args) if \
            session.attendance_closed_time and time_now <= session.attendance_closed_time else None
