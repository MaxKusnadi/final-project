from app.models.course import Course
from app.controller.utils.checker import Checker
from app.controller.utils.utils import Utils
from app import logger, cache


class CourseController:

    @cache.memoize()
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

    @cache.memoize()
    def get_course_info(self, course_id):
        logger.info("Getting course info for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        d = Utils.get_course_info(course)
        d['status'] = 200
        return d

    @cache.memoize()
    def _get_course(self, course_id):
        course = Course.query.filter(Course.id == int(course_id)).first()
        return course

    @cache.memoize()  #TODO update this next time
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

    @cache.memoize()  #TODO update this next time
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

    @cache.memoize()  #TODO update this next time
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

