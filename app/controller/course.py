from app.models.course import Course, CourseStudent, CourseStaff
from app.models.user import User
from app.controller.utils.checker import Checker
from app.controller.utils.utils import Utils
from app import db, logger


class CourseController:

    def get_users_courses(self, user):
        logger.info("Getting all courses of user {}".format(user.name))

        course_taken = user.courses_taken
        course_taken = list(map(lambda x: Utils.get_course_info(x.course), course_taken))
        course_taught = user.courses_taught
        course_taught = list(map(lambda x: Utils.get_course_info(x.course), course_taught))

        d = dict()
        d['course_taken'] = course_taken
        d['course_taught'] = course_taught
        d['status'] = 200
        return d

    def get_course_info(self, course_id):
        logger.info("Getting course info for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def _get_course(self, course_id):
        course = Course.query.filter(Course.id == int(course_id)).first()
        return course

    def create_mock_course(self, **kwargs):
        logger.info("Creating a mocked course")
        course_id = kwargs.get("course_code")

        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        course = Course("dummy_id", "Prof Dummy", "dummy_id", course_id,
                        "Introduction to dummy module", "2017/2018", 1)
        course.is_mocked = True
        db.session.add(course)
        db.session.commit()
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    def get_mock_users_courses(self, matric):
        logger.info("Getting all courses of a user")
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        return self.get_users_courses(user)

    def get_mock_course_info(self, course_id):
        logger.info("Getting mock course info for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        return self.get_course_info(course_id)

    def mock_user_join_course(self, course_id, **kwargs):
        matric = kwargs.get("matric")
        role = kwargs.get('role', 0)
        logger.info("User {} joins course {}".format(matric, course_id))

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user, matric)
        if error:
            return error

        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
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

    def get_mock_course_student(self, course_id):
        logger.info("Getting mock course student for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        return self.get_course_student(course_id)

    def get_course_student(self, course_id):
        logger.info("Getting course student for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        course_students = course.students
        course_students = list(map(lambda x: Utils.get_user_info(x.user), course_students))
        d = dict()
        d['results'] = course_students
        d['status'] = 200
        return d

    def get_mock_course_staff(self, course_id):
        logger.info("Getting mock course staff for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        return self.get_course_staff(course_id)

    def get_course_staff(self, course_id):
        logger.info("Getting course staff for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        course_staffs = course.staffs
        course_staffs = list(map(lambda x: Utils.get_user_info(x.user), course_staffs))
        d = dict()
        d['results'] = course_staffs
        d['status'] = 200
        return d

    def get_mock_course_group(self, course_id):
        logger.info("Getting course group for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        return self.get_course_group(course_id)

    def get_course_group(self, course_id):
        logger.info("Getting course group for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error

        course_groups = course.groups
        course_groups = list(map(lambda x: Utils.get_group_info(x), course_groups))
        d = dict()
        d['results'] = course_groups
        d['status'] = 200
        return d

