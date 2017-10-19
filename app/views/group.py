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

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/group request")
        group_name = request.args.get('group_name')
        group_type = request.args.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
        result = self.control.get_group_info(course_code, group_name, group_type)
        return json.dumps(result)


class GroupStudentView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/group/students request")
        group_name = request.args.get('group_name')
        group_type = request.args.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
        result = self.control.get_group_student(course_code, group_name, group_type)
        return json.dumps(result)


class GroupStaffView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, course_code):
        logging.info("New GET/course/<string:course_code>/group/staffs request")
        group_name = request.args.get('group_name')
        group_type = request.args.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
        result = self.control.get_group_staff(course_code, group_name, group_type)
        return json.dumps(result)


app.add_url_rule('/groups', view_func=GroupView.as_view('group'), methods=['GET'])
app.add_url_rule('/course/<string:course_code>/group', view_func=IndividualGroupView.as_view('individual_group'),
                 methods=['GET'])
app.add_url_rule('/course/<string:course_code>/group/students', view_func=GroupStudentView.as_view('group_student'))
app.add_url_rule('/course/<string:course_code>/group/staffs', view_func=GroupStaffView.as_view('group_staff'))
