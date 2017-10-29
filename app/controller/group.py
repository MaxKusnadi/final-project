import logging

from app.models.course import Course, CourseStaff
from app.models.group import Group, GroupStudent, GroupStaff
from app.models.user import User
from app.controller.utils.utils import Utils
from app.controller.utils.checker import Checker
from app import db


class GroupController:

    def check_staff_group(self, user):
        logging.info("Checking which course {} has not linked to".format(user.name))
        course_staff = CourseStaff.query.filter(CourseStaff.user_id == user.id,
                                                CourseStaff.is_attached_to_group == False).all()
        module_info = list(map(lambda x: Utils.get_course_info(x.course), course_staff))
        d = dict()
        d['status'] = 200
        d['result'] = module_info
        return d

    def create_mock_group(self, **kwargs):
        logging.info("Creating a mocked group")
        course_code = kwargs.get("course_code")
        group_name = kwargs.get("group_name")

        course = self._get_course(course_code)
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

    def create_group_staff(self, course_id, user, group_id):
        logging.info("Linking {} with a group from {}".format(user.name, course_id))

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
        logging.info("Unlinking {} with a group from {}".format(user.name, course_id))

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

    def get_group_info(self, course_id, group_id):
        logging.info("Getting group info for {}".format(course_id))
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

    def _get_group(self, course, group_id):
        group = Group.query.filter(Group.id == int(group_id),
                                   Group.course_id == int(course.id)).first()
        return group

    def _get_course(self, course_id):
        course = Course.query.filter(Course.id == int(course_id)).first()
        return course

    def get_all_groups(self, course_id):
        logging.info("Getting all groups info for {}".format(course_id))
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

    def get_mock_group_info(self, course_code, group_id):
        logging.info("Getting mock group info for {}".format(course_code))
        course = self._get_course(course_code)
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = self._get_group(course, group_id)
        error = Checker.check_mock_group(group, course_code, group_id)
        if error:
            return error

        return self.get_group_info(course_code, group_id)

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

        course = self._get_course(course_code)
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = self._get_group(course, group_name)
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
        course = self._get_course(course_code)
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = self._get_group(course, group_name)
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error
        return self.get_group_student(course_code, group_name)

    def get_group_student(self, course_id, group_id):
        logging.info("Getting group {} students for {}".format(group_id, course_id))
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

    def get_mock_group_staff(self, course_code, group_name, group_type):
        logging.info("Getting mock group {} students for {}".format(group_name, course_code))
        course = self._get_course(course_code)
        error = Checker.check_course(course, course_code)
        if error:
            return error
        group = self._get_group(course, group_name)
        error = Checker.check_mock_group(group, course_code, group_name, group_type)
        if error:
            return error
        return self.get_group_staff(course_code, group_name)

    def get_group_staff(self, course_id, group_id):
        logging.info("Getting group {} students for {}".format(group_id, course_id))
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

# if __name__ == '__main__':
#     error = Checker.check_group(None, 1, 2)
#     print(error)