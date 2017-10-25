import logging
import json

from flask.views import MethodView
from flask_login import login_required, current_user
from flask import request

from app import app
from app.controller.group import GroupController
from app.constants.error import Error


class GroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self):
        logging.info("New GET /group request")
        result = self.control.get_users_groups(current_user)
        return json.dumps(result)


class IndividualGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, course_id, group_id):
        logging.info("New GET /course/<string:course_id>/group/<int:group_id request")
        result = self.control.get_group_info(course_id, group_id)
        return json.dumps(result)


class AllGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, course_id):
        logging.info("New GET /course/<string:course_id>/groups request")
        result = self.control.get_all_groups(course_id)
        return json.dumps(result)


class GroupStudentView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, course_id, group_id):
        logging.info("New GET /course/<string:course_id>/group/<int:group_id/students request")
        result = self.control.get_group_student(course_id, group_id)
        return json.dumps(result)


class GroupStaffView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def post(self, course_id, group_id):
        logging.info("New POST /course/<string:course_id>/group/<int:group_id/staffs request")

        result = self.control.create_group_staff(course_id, current_user, group_id)
        return json.dumps(result)

    def get(self, course_id, group_id):
        logging.info("New GET/course/<string:course_id>/group/<int:group_id/staffs request")
        result = self.control.get_group_staff(course_id, group_id)
        return json.dumps(result)

    def delete(self, course_id, group_id):
        logging.info("New DELETE/course/<string:course_id>/group/<int:group_id/staffs request")
        result = self.control.delete_group_staff(course_id, current_user, group_id)
        return json.dumps(result)


class CheckStaffGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self):
        logging.info("New GET /check-group request")
        result = self.control.check_staff_group(current_user)
        return json.dumps(result)


app.add_url_rule('/groups', view_func=GroupView.as_view('group'), methods=['GET'])
app.add_url_rule('/check-group', view_func=CheckStaffGroupView.as_view('check_group'), methods=['GET'])
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>', view_func=IndividualGroupView.as_view('individual_group'),
                 methods=['GET'])
app.add_url_rule('/course/<int:course_id>/groups', view_func=AllGroupView.as_view('all_group'))
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>/students', view_func=GroupStudentView.as_view('group_student'))
app.add_url_rule('/course/<int:course_id>/group/<int:group_id>/staffs', view_func=GroupStaffView.as_view('group_staff'))
