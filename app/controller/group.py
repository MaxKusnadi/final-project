import logging

from app.models.course import Course, CourseStudent, CourseStaff
from app.models.group import Group, GroupStudent, GroupStaff
from app.models.week_code import WeekCode
from app.models.user import User
from app.controller.utils import Utils
from app.constants.error import Error
from app import db


class GroupController:

    def create_group(self, **kwargs):
        logging.info("Creating a mocked group")
        course_code = kwargs.get("course_code")
        group_name = kwargs.get("group_name")

        course = Course.query.filter(Course.course_code == course_code).first()
        if not course:
            d = Utils.create_error_code(Error.COURSE_NOT_FOUND, course_code)
            return d
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.course_name == course.course_name).first()
        if group:
            d = Utils.create_error_code(Error.GROUP_EXIST, group_name)
            return d
        group = Group(course, group_name, "1500", "1600", 2, 0, "SOC", "Lecture")
        group.is_mocked = True
        db.session.add(group)
        db.session.commit()
        d = self._get_group_info(group)
        d['status'] = 200
        return d

    def get_users_groups(self, metric):
        logging.info("Getting all groups for user {}".format(metric))
        user = User.query.filter(User.metric == metric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, metric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, metric)
            return d
        groups_taken = user.groups
        groups_taken = list(map(lambda x: self._get_group_info(x.group), groups_taken))
        groups_taught = user.groups_taught
        groups_taught = list(map(lambda x: self._get_group_info(x.group), groups_taught))

        d = dict()
        d['group_taken'] = groups_taken
        d['group_taught'] = groups_taught
        d['status'] = 200
        return d

    def get_group_info(self, course_code, group_name, group_type):
        logging.info("Getting group info for {}".format(course_code))
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course.course_code == course_code).first()
        if not group:
            d = Utils.create_error_code(Error.GROUP_NOT_FOUND, course_code, group_name, group_type)
            return d
        d = self._get_group_info(group)
        d['status'] = 200
        return d

    def user_join_group(self, course_code, **kwargs):
        metric = kwargs.get("metric")
        role = kwargs.get('role', 0)
        group_name = kwargs.get('group_name')
        group_type = kwargs.get('group_type')
        logging.info("User {} joins group {} course {}".format(metric, group_name, course_code))

        user = User.query.filter(User.metric == metric).first()
        if not user:
            d = Utils.create_error_code(Error.USER_NOT_FOUND, metric)
            return d
        if not user.is_mocked:
            d = Utils.create_error_code(Error.USER_NOT_MOCKED, metric)
            return d

        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course.course_code == course_code).first()
        if not group:
            d = Utils.create_error_code(Error.GROUP_NOT_FOUND, course_code, group_name, group_type)
            return d

        role = int(role)
        if role == 1:
            a = GroupStaff(user, group)
        else:
            a = GroupStudent(user, group)
        db.session.add(a)
        db.session.commit()
        d = dict()
        d['text'] = "Success"
        return d

    def get_group_student(self, course_code, group_name, group_type):
        logging.info("Getting group {} students for {}".format(group_name, course_code))
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course.course_code == course_code).first()
        if not group:
            d = Utils.create_error_code(Error.GROUP_NOT_FOUND, course_code, group_name, group_type)
            return d
        group_students = group.students
        group_students = list(map(lambda x: self._get_user_info(x.user), group_students))
        d = dict()
        d['results'] = group_students
        d['status'] = 200
        return d

    def get_group_staff(self, course_code, group_name, group_type):
        logging.info("Getting group {} students for {}".format(group_name, course_code))
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course.course_code == course_code).first()
        if not group:
            d = Utils.create_error_code(Error.GROUP_NOT_FOUND, course_code, group_name, group_type)
            return d
        group_staffs = group.staffs
        group_staffs = list(map(lambda x: self._get_user_info(x.user), group_staffs))
        d = dict()
        d['results'] = group_staffs
        d['status'] = 200
        return d

    def _get_group_info(self, group):
        d = dict()
        d['group_name'] = group.group_name
        d['course_code'] = group.course.course_code
        d['start_time'] = group.start_time
        d['end_time'] = group.end_time
        d['day_code'] = group.day_code
        d['week_code'] = WeekCode.query.filter(WeekCode.week_code == group.week_code).first().description
        d['venue'] = group.venue
        d['group_type'] = group.group_type
        return d

    def _get_user_info(self, user):
        d = dict()
        d['name'] = user.name
        d['metric'] = user.metric
        d['email'] = user.email
        return d
