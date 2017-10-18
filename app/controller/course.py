import logging

from app.models.course import Course, CourseStudent, CourseStaff
from app.models.user import User
from app.controller.utils.checker import Checker
from app.controller.utils.utils import Utils
from app.constants.error import Error
from app import db


class MockCourseController:

    def create_course(self, **kwargs):
        logging.info("Creating a mocked course")
        course_code = kwargs.get("course_code")

        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course_exist(course)
        if error:
            return error

        course = Course("dummy_id", "Prof Dummy", "dummy_id", course_code,
                        "Introduction to dummy module", "2017/2018", 1)
        course.is_mocked = True
        db.session.add(course)
        db.session.commit()
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def get_users_courses(self, matric):
        logging.info("Getting all courses of a user")
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

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
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def user_join_course(self, course_code, **kwargs):
        matric = kwargs.get("matric")
        role = kwargs.get('role', 0)
        logging.info("User {} joins course {}".format(matric, course_code))

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error

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
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error

        course_students = course.students
        course_students = list(map(lambda x: Utils.get_user_info(x.user), course_students))
        d = dict()
        d['results'] = course_students
        d['status'] = 200
        return d

    def get_course_staff(self, course_code):
        logging.info("Getting course staff for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error

        course_staffs = course.staffs
        course_staffs = list(map(lambda x: Utils.get_user_info(x.user), course_staffs))
        d = dict()
        d['results'] = course_staffs
        d['status'] = 200
        return d

    def get_course_group(self, course_code):
        logging.info("Getting course group for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error

        course_groups = course.groups
        course_groups = list(map(lambda x: Utils.get_group_info(x), course_groups))
        d = dict()
        d['results'] = course_groups
        d['status'] = 200
        return d

