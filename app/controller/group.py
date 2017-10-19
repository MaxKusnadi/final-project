import logging

from app.models.course import Course
from app.models.group import Group, GroupStudent, GroupStaff
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db


class GroupController:

    def create_mock_group(self, **kwargs):
        logging.info("Creating a mocked group")
        course_code = kwargs.get("course_code")
        group_name = kwargs.get("group_name")

        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_mock_course(course, course_code)
        if error:
            return error

        group = Group.query.filter(Group.group_name == group_name,
                                   Group.course_name == course.course_name).first()
        error = Checker.check_group_exist(group)
        if error:
            return error

        group = Group(course, group_name, "1500", "1600", 2, 0, "SOC", "Lecture")
        group.is_mocked = True
        db.session.add(group)
        db.session.commit()
        d = Utils.get_group_info(group)
        d['status'] = 200
        return d

    def get_users_groups(self, user):
        logging.info("Getting all groups for user {}".format(user.name))

        groups_taken = user.groups
        groups_taken = list(map(lambda x: Utils.get_group_info(x.group), groups_taken))
        groups_taught = user.groups_taught
        groups_taught = list(map(lambda x: Utils.get_group_info(x.group), groups_taught))

        d = dict()
        d['group_taken'] = groups_taken
        d['group_taught'] = groups_taught
        d['status'] = 200
        return d

    def get_mock_users_groups(self, matric):
        logging.info("Getting all mocked groups for user {}".format(matric))
        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user)
        if error:
            return error

        return self.get_users_groups(user)

    def get_group_info(self, course_code, group_name, group_type):
        logging.info("Getting group info for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_code, group_name, group_type)
        if error:
            return error

        d = Utils.get_group_info(group)
        d['status'] = 200
        return d

    def get_mock_group_info(self, course_code, group_name, group_type):
        logging.info("Getting mock group info for {}".format(course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error

        return self.get_group_info(course_code, group_name, group_type)

    def mock_user_join_group(self, course_code, **kwargs):
        matric = kwargs.get("matric")
        role = kwargs.get('role', 0)
        group_name = kwargs.get('group_name')
        group_type = kwargs.get('group_type')
        logging.info("User {} joins group {} course {}".format(matric, group_name, course_code))

        user = User.query.filter(User.matric == matric).first()
        error = Checker.check_mock_user(user)
        if error:
            return error

        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error

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

    def get_mock_group_student(self, course_code, group_name, group_type):
        logging.info("Getting mock group {} students for {}".format(group_name, course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error
        return self.get_group_student(course_code, group_name, group_type)

    def get_group_student(self, course_code, group_name, group_type):
        logging.info("Getting group {} students for {}".format(group_name, course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_code, group_name, group_type)
        if error:
            return error

        group_students = group.students
        group_students = list(map(lambda x: Utils.get_user_info(x.user), group_students))
        d = dict()
        d['results'] = group_students
        d['status'] = 200
        return d

    def get_mock_group_staff(self, course_code, group_name, group_type):
        logging.info("Getting mock group {} students for {}".format(group_name, course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error
        return self.get_group_staff(course_code, group_name, group_type)

    def get_group_staff(self, course_code, group_name, group_type):
        logging.info("Getting group {} students for {}".format(group_name, course_code))
        course = Course.query.filter(Course.course_code == course_code).first()
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = Group.query.filter(Group.group_name == group_name,
                                   Group.group_type == group_type,
                                   Group.course_id == course.id).first()
        error = Checker.check_group(group, course_code, group_name, group_type)
        if error:
            return error
        group_staffs = group.staffs
        group_staffs = list(map(lambda x: Utils.get_user_info(x.user), group_staffs))
        d = dict()
        d['results'] = group_staffs
        d['status'] = 200
        return d
