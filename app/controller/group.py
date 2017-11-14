from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStaff
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db, logger, cache


class GroupController:

    def check_staff_group(self, user):
        logger.info("Checking which course {} has not linked to".format(user.name))
        course_staff = CourseStaff.query.filter(CourseStaff.user_id == user.id,
                                                CourseStaff.is_attached_to_group == False).all()
        module_info = list(map(lambda x: Utils.get_course_info(x.course), course_staff))
        d = dict()
        d['status'] = 200
        d['result'] = module_info
        return d

    def create_group_staff(self, course_id, user, group_id):
        logger.info("Linking {} with a group from {}".format(user.name, course_id))

        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error

        error = Checker.check_is_user_staff_course(user, course)
        if error:
            return error

        group_staff = GroupStaff.query.filter(GroupStaff.user_id == user.id,
                                              GroupStaff.group_id == group.id).first()
        if not group_staff:
            group_staff = GroupStaff(user, group)
            db.session.add(group_staff)
            db.session.commit()

        course_staff = CourseStaff.query.filter(CourseStaff.course_id == course_id,
                                                CourseStaff.user_id == user.id).first()
        course_staff.is_attached_to_group = True
        db.session.commit()

        d = dict()
        d['status'] = 200
        d['text'] = "Successful"
        return d

    def delete_group_staff(self, course_id, user, group_id):
        logger.info("Unlinking {} with a group from {}".format(user.name, course_id))

        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error

        error = Checker.check_is_user_staff_course(user, course)
        if error:
            return error

        group_staff = GroupStaff.query.filter(GroupStaff.user_id == user.id,
                                              GroupStaff.group_id == group.id).first()
        if group_staff:
            db.session.delete(group_staff)
            db.session.commit()

        d = dict()
        d['status'] = 200
        d['text'] = "Successful"
        return d

    def get_users_groups(self, user):
        logger.info("Getting all groups for user {}".format(user.name))

        groups_taken = user.groups
        groups_taken = list(map(lambda x: x.group, groups_taken))
        groups_taken = list(filter(lambda x: x.day_code != -1, groups_taken))
        groups_taken = sorted(groups_taken, key=lambda x: x.start_time)
        groups_taken = sorted(groups_taken, key=lambda x: x.day_code)
        groups_taken = list(map(lambda x: Utils.get_group_info(x), groups_taken))

        groups_taught = user.groups_taught
        groups_taught = list(map(lambda x: x.group, groups_taught))
        groups_taught = list(filter(lambda x: x.day_code != -1, groups_taught))
        groups_taught = sorted(groups_taught, key=lambda x: x.start_time)
        groups_taught = sorted(groups_taught, key=lambda x: x.day_code)
        groups_taught = list(map(lambda x: Utils.get_group_info(x), groups_taught))

        d = dict()
        d['group_taken'] = groups_taken
        d['group_taught'] = groups_taught
        d['status'] = 200
        return d

    @cache.memoize()
    def get_group_info(self, course_id, group_id):
        logger.info("Getting group info for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error

        d = Utils.get_group_info(group)
        d['status'] = 200
        return d

    @cache.memoize(600)
    def _get_group(self, course, group_id):
        group = Group.query.filter(Group.id == int(group_id),
                                   Group.course_id == int(course.id)).first()
        return group

    @cache.memoize(600)
    def _get_course(self, course_id):
        course = Course.query.filter(Course.id == int(course_id)).first()
        return course

    @cache.memoize(600)
    def get_all_groups(self, course_id):
        logger.info("Getting all groups info for {}".format(course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        groups = course.groups
        groups_info = list(map(lambda x: Utils.get_group_info(x), groups))
        d = dict()
        d['groups'] = groups_info
        d['status'] = 200
        return d

    def get_group_student(self, course_id, group_id):
        logger.info("Getting group {} students for {}".format(group_id, course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error

        group_students = group.students
        group_students = list(map(lambda x: Utils.get_user_info(x.user), group_students))
        d = dict()
        d['results'] = group_students
        d['status'] = 200
        return d

    def get_group_staff(self, course_id, group_id):
        logger.info("Getting group {} students for {}".format(group_id, course_id))
        course = self._get_course(course_id)
        error = Checker.check_course(course, course_id)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_group(group, course_id, group_id)
        if error:
            return error
        group_staffs = group.staffs
        group_staffs = list(map(lambda x: Utils.get_user_info(x.user), group_staffs))
        d = dict()
        d['results'] = group_staffs
        d['status'] = 200
        return d
