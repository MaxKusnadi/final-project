import logging

from app.models.course import Course, CourseStudent, CourseStaff
from app.models.user import User
from app.controller.utils import Utils
from app.constants.error import Error
from app import db


class MockCourseController:

    def create_course(self, **kwargs):
        logging.info("Creating a mocked course")
        course_code = kwargs.get("course_code")

        course = Course.query.filter(Course.course_code == course_code).first()
        if course:
            d = Utils.create_error_code(Error.COURSE_EXIST, course_code)
            return d
        course = Course("dummy_id", "Prof Dummy", "dummy_id", course_code,
                        "Introduction to dummy module", "2017/2018", 1)
        course.is_mocked = True
        db.session.add(course)
        db.session.commit()
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def get_users_courses(self, metric):
        logging.info("Getting all courses of a user")
        user = User.query.filter(User.metric == metric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, metric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, metric)
            return d
        course_taken = user.course_taken
        course_taken = list(map(lambda x: Utils.get_course_info(x.course), course_taken))
        course_taught = user.course_taught
        course_taught = list(map(lambda x: Utils.get_course_info(x.course), course_taught))

        d = dict()
        d['course_taken'] = course_taken
        d['course_taught'] = course_taught
        d['status'] = 200
        return d

    def get_course_info(self, course_code):
        logging.info("Getting course info for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        if not course.is_mocked:
            d = Utils.create_error_code(Error.COURSE_NOT_MOCKED, course_code)
            return d
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def user_join_course(self, course_code, **kwargs):
        metric = kwargs.get("metric")
        role = kwargs.get('role', 0)
        logging.info("User {} joins course {}".format(metric, course_code))

        user = User.query.filter(User.metric == metric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, metric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, metric)
            return d

        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        if not course.is_mocked:
            d = Utils.create_error_code(Error.COURSE_NOT_MOCKED, course_code)
            return d

        role = int(role)
        if role == 1:
            a = CourseStaff(user, course)
        else:
            a = CourseStudent(user, course)
        db.session.add(a)
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        return d

    def get_course_student(self, course_code):
        logging.info("Getting course student for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        if not course.is_mocked:
            d = Utils.create_error_code(Error.COURSE_NOT_MOCKED, course_code)
            return d

        course_students = course.students
        course_students = list(map(lambda x: Utils.get_user_info(x.user), course_students))
        d = dict()
        d['results'] = course_students
        d['status'] = 200
        return d

    def get_course_staff(self, course_code):
        logging.info("Getting course staff for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        if not course.is_mocked:
            d = Utils.create_error_code(Error.COURSE_NOT_MOCKED, course_code)
            return d
        course_staffs = course.staffs
        course_staffs = list(map(lambda x: Utils.get_user_info(x.user), course_staffs))
        d = dict()
        d['results'] = course_staffs
        d['status'] = 200
        return d

    def get_course_group(self, course_code):
        logging.info("Getting course group for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        if not course.is_mocked:
            d = Utils.create_error_code(Error.COURSE_NOT_MOCKED, course_code)
            return d
        course_groups = course.groups
        course_groups = list(map(lambda x: Utils.get_group_info(x), course_groups))
        d = dict()
        d['results'] = course_groups
        d['status'] = 200
        return d

