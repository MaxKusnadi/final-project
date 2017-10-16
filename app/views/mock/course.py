import logging
import json

from flask.views import MethodView
from flask import request

from app import app
from app.controller.course import CourseController
from app.constants.error import Error


class CourseView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def post(self):
        logging.info("New POST /mock/course request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("course_code"):
            return json.dumps(Error.COURSE_CODE_NOT_FOUND)
        result = self.control.create_course(**data)
        return json.dumps(result)

    def get(self, course_code):
        logging.info("New GET /mock/course request")
        if course_code is None:
            metric = request.args.get('metric')
            if not metric:
                return json.dumps(Error.METRIC_NOT_FOUND)
            result = self.control.get_users_courses(metric)
        else:
            result = self.control.get_course_info(course_code)
        return json.dumps(result)


class JoinCourseView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def post(self, course_code):
        logging.info("New POST mock/join/course/ request")
        data = request.get_json()

        if not data:
            return json.dumps(Error.JSON_NOT_FOUND)
        if not data.get("metric"):
            return json.dumps(Error.METRIC_NOT_FOUND)

        result = self.control.user_join_course(course_code, **data)
        return json.dumps(result)


class CourseStudentView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /mock/course/<string:course_code>/students request")
        result = self.control.get_course_student(course_code)
        return json.dumps(result)


class CourseStaffView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /mock/course/<string:course_code>/staffs request")
        result = self.control.get_course_staff(course_code)
        return json.dumps(result)


class CourseGroupView(MethodView):

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /mock/course/<string:course_code>/groups request")
        result = self.control.get_course_group(course_code)
        return json.dumps(result)


course_view = CourseView.as_view('mock_course')
app.add_url_rule('/mock/course', view_func=course_view, methods=['POST'])
app.add_url_rule('/mock/course', defaults={'course_code': None}, view_func=course_view, methods=['GET'])
app.add_url_rule('/mock/course/<string:course_code>', view_func=course_view, methods=['GET'])
app.add_url_rule('/mock/join/course/<string:course_code>', view_func=JoinCourseView.as_view('mock_join_course'))
app.add_url_rule('/mock/course/<string:course_code>/students', view_func=CourseStudentView.as_view('mock_course_student'))
app.add_url_rule('/mock/course/<string:course_code>/staffs', view_func=CourseStaffView.as_view('mock_course_staff'))
app.add_url_rule('/mock/course/<string:course_code>/groups', view_func=CourseGroupView.as_view('mock_course_group'))

