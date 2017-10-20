import logging
import json

from flask.views import MethodView
from flask_login import login_required, current_user

from app import app
from app.controller.course import CourseController


class CourseView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /course request")
        if course_code is None:
            result = self.control.get_users_courses(current_user)
        else:
            result = self.control.get_course_info(course_code)
        return json.dumps(result)


class CourseStudentView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/students request")
        result = self.control.get_course_student(course_code)
        return json.dumps(result)


class CourseStaffView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/staffs request")
        result = self.control.get_course_staff(course_code)
        return json.dumps(result)


class CourseGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = CourseController()

    def get(self, course_code):
        logging.info("New GET /course/<string:course_code>/groups request")
        result = self.control.get_course_group(course_code)
        return json.dumps(result)


course_view = CourseView.as_view('course')
app.add_url_rule('/course', defaults={'course_code': None}, view_func=course_view, methods=['GET'])
app.add_url_rule('/course/<string:course_code>', view_func=course_view, methods=['GET'])
app.add_url_rule('/course/<string:course_code>/students', view_func=CourseStudentView.as_view('course_student'))
app.add_url_rule('/course/<string:course_code>/staffs', view_func=CourseStaffView.as_view('course_staff'))
app.add_url_rule('/course/<string:course_code>/groups', view_func=CourseGroupView.as_view('course_group'))

