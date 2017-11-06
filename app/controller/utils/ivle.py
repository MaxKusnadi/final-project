import requests

from app.models.week_code import WeekCode
from app.constants.ivle import (API_KEY, IVLE_URL, MODULE_URL, PROFILE_URL, VALIDATE_URL,
                                CLASS_ROSTER_URL, STUDENT_GROUP_URL, LECTURER_URL,
                                STAFF_GROUP_URL)
from app import logger


class IVLEScrapper:

    def get_user_courses(self, token):
        logger.info("Getting user modules")
        results = IVLEApi.get_modules(token)
        teaching_modules = filter(lambda x: x['Permission'] != 'S', results)
        student_modules = filter(lambda x: x['Permission'] == 'S', results)
        d = dict()
        d['modules_taken'] = list(map(lambda x: self._get_module_info(x), student_modules))
        d['modules_taught'] = list(map(lambda x: self._get_module_info(x), teaching_modules))
        return d

    def get_class_roster(self, token, course_id):
        logger.info("Getting class roster for Course {}".format(course_id))
        results = IVLEApi.get_class_roster(token, course_id)
        return list(map(lambda x: self._get_user_info(x), results))

    def get_student_groups(self, token, course_id):
        logger.info("Getting student groups for Course {}".format(course_id))
        results = IVLEApi.get_student_group(token, course_id)
        return list(map(lambda x: self._get_group_info(x), results))

    def get_staff_groups(self, token, course_id):
        logger.info("Getting staff groups for Course {}".format(course_id))
        results = IVLEApi.get_staff_group(token, course_id)
        return list(map(lambda x: self._get_staff_group_info(x), results))

    def get_course_staffs(self, token, course_id):
        logger.info("Getting staffs for Course {}".format(course_id))
        result = IVLEApi.get_course_staffs(token, course_id)
        return list(map(lambda x: self._get_staff_info(x), result))

    def _get_staff_info(self, staff):
        d = {
            "name": staff['User']['Name'],
            "email": staff['User']['Email'],
            "matric": staff['User']["UserID"],
            "role": staff['Role'].strip()
        }
        return d

    def _get_group_info(self, group):
        d = {
            'group_name': group['ClassNo'],
            'start_time': str(group['StartTime']).zfill(4),
            'end_time': str(group['EndTime']).zfill(4),
            'venue': group['Venue'],
            'group_type': group['LessonType']
        }
        try:
            d['day_code'] = int(group['DayCode'])
            d['week_code'] = int(group['WeekCode'])
        except ValueError:
            d['day_code'] = -1
            d['week_code'] = -1
        return d

    def _get_staff_group_info(self, group):
        group_time = group['Time']
        start_time, end_time = group_time.split(" - ") if group_time else ("0", "0")
        d = {
            'group_name': group['GroupName'],
            'start_time': start_time.zfill(4),
            'end_time': end_time.zfill(4),
            'venue': group['Venue'],
            'group_type': group['GroupType'].upper()
        }
        try:
            d['day_code'] = self._get_day_code(group["Day"]) if group['Day'] else -1
            d['week_code'] = self._get_week_code(group['Week']) if group['Week'] else -1
        except ValueError:
            d['day_code'] = -1
            d['week_code'] = -1
        return d

    def _get_module_info(self, course):
        d = {
            'course_id': course['ID'],
            'course_code': course['CourseCode'],
            'course_name': course['CourseName'],
            'acad_year': course['CourseAcadYear'],
            'semester': int(course['CourseSemester'].split(' ')[-1]),
            'permission': course['Permission']
        }
        try:
            d['creator_user_id'] = course['Creator']['UserID']
            d['creator_name'] = course['Creator']['Name']
        except TypeError:
            d['creator_user_id'] = ""
            d['creator_name'] = ""
        return d

    def _get_user_info(self, user):
        d = {
            'name': user['Name'],
            'email': user['Email'],
            'matric': user['UserID']
        }
        return d

    def _get_day_code(self, day):
        days = ['Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for idx, val in enumerate(days):
            if val == day:
                return idx + 1

    def _get_week_code(self, week_desc):
        week = WeekCode.query.filter(WeekCode.description == week_desc.upper()).first()
        return week.week_code


class IVLEApi:

    @staticmethod
    def get_student_group(token, course_id):
        url = IVLE_URL + STUDENT_GROUP_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token,
            "CourseID": course_id
        }
        resp = requests.get(url, params=params).json()
        return resp['Results']

    @staticmethod
    def get_staff_group(token, course_id):
        url = IVLE_URL + STAFF_GROUP_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token,
            "CourseID": course_id,
            "AcadYear": "2017/2018",
            "Semester": 1
        }
        resp = requests.get(url, params=params).json()
        return resp['Results']

    @staticmethod
    def get_class_roster(token, course_id):
        url = IVLE_URL + CLASS_ROSTER_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token,
            "CourseID": course_id
        }
        resp = requests.get(url, params=params).json()
        return resp['Results']

    @staticmethod
    def get_modules(token):
        url = IVLE_URL + MODULE_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token,
            "Duration": 0,
            "IncludeAllInfo": False
        }
        resp = requests.get(url, params=params).json()
        return resp['Results']

    @staticmethod
    def validate_token(token):
        validate_url = IVLE_URL + VALIDATE_URL
        params = {
            "APIKey": API_KEY,
            "Token": token
        }
        resp = requests.get(validate_url, params=params).json()
        return resp['Success'], resp['Token']

    @staticmethod
    def get_profile(token):
        url = IVLE_URL + PROFILE_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token
        }
        resp = requests.get(url, params=params).json()
        return resp['Results'][0]

    @staticmethod
    def get_course_staffs(token, course_id):
        url = IVLE_URL + LECTURER_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": token,
            "CourseID": course_id,
            "Duration": 0
        }
        resp = requests.get(url, params=params).json()
        return resp['Results']

