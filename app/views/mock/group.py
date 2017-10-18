import logging
import json

from flask.views import MethodView
from flask import request

from app import app
from app.controller.group import MockGroupController
from app.constants.error import Error


class GroupView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockGroupController()

    def post(self):
        logging.info("New POST /mock/group request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("course_code"):
            return json.dumps(Error.COURSE_CODE_NOT_FOUND)
        if not data.get("group_name"):
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        result = self.control.create_group(**data)
        return json.dumps(result)

    def get(self, course_code):
        logging.info("New GET /mock/group request")
        if course_code is None:
            matric = request.args.get('matric')
            if not matric:
                return json.dumps(Error.MATRIC_NOT_FOUND)
            result = self.control.get_users_groups(matric)
        else:
            group_name = request.args.get('group_name')
            group_type = request.args.get('group_type')
            if not group_name:
                return json.dumps(Error.GROUP_NAME_NOT_FOUND)
            if not group_type:
                return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
            result = self.control.get_group_info(course_code, group_name, group_type)
        return json.dumps(result)


class JoinGroupView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockGroupController()

    def post(self, course_code):
        logging.info("New POST mock/join/group/ request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("matric"):
            return json.dumps(Error.MATRIC_NOT_FOUND)

        group_name = data.get('group_name')
        group_type = data.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)

        result = self.control.user_join_group(course_code, **data)
        return json.dumps(result)


class GroupStudentView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = MockGroupController()

    def get(self, course_code):
        logging.info("New GET /mock/group/<string:course_code>/students request")
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
        self.control = MockGroupController()

    def get(self, course_code):
        logging.info("New GET /mock/group/<string:course_code>/staffs request")
        group_name = request.args.get('group_name')
        group_type = request.args.get('group_type')
        if not group_name:
            return json.dumps(Error.GROUP_NAME_NOT_FOUND)
        if not group_type:
            return json.dumps(Error.GROUP_TYPE_NOT_FOUND)
        result = self.control.get_group_staff(course_code, group_name, group_type)
        return json.dumps(result)


group_view = GroupView.as_view('mock_group')
app.add_url_rule('/mock/group', view_func=group_view, methods=['POST'])
app.add_url_rule('/mock/group', defaults={'course_code': None}, view_func=group_view, methods=['GET'])
app.add_url_rule('/mock/group/<string:course_code>', view_func=group_view, methods=['GET'])
app.add_url_rule('/mock/join/group/<string:course_code>', view_func=JoinGroupView.as_view('mock_join_group'))
app.add_url_rule('/mock/group/<string:course_code>/students', view_func=GroupStudentView.as_view('mock_group_student'))
app.add_url_rule('/mock/group/<string:course_code>/staffs', view_func=GroupStaffView.as_view('mock_group_staff'))
