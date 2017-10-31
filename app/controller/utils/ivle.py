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
        if not group_time:
            logger.critical("ERROR FOUND WHEN PARSING THIS {}".format(group))
        start_time, end_time = group_time.split(" - ") if group_time else ("0", "0")
        d = {
            'group_name': group['GroupName'],
            'start_time': start_time.zfill(4),
            'end_time': end_time.zfill(4),
            'venue': group['Venue'],
            'group_type': group['GroupType'].upper()
        }
        try:
            d['day_code'] = self._get_day_code(group["Day"])
            d['week_code'] = self._get_week_code(group['Week'])
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


# if __name__ == '__main__':
#     TOKEN = "36C5E5A0DAEEEFFDE451284055243FD1BAC5B957FD6EF2708290B454946D7B3246D675ECDA538638ECB96E25934984BF8BFEB8AFF005B0A98C959C3D1BA146334AC33453117EF1F69AB5177AEF1EABBB6BAB8D73088FE46CB1D642A8563290866093F1667B6ECB991F3FCCCD54B1E7C08147369D34B1F091D983763C6A0B70FA89B5BA60802F32F86A9485CD655AFFC86081C316699E41271F2634F3FCB0E9CA418450F1BD66C7D0259B8A59FD8F5E364CA9F2CC7C070C2D84B23FFA88BD23BF48B4A4A1271C5430AAE4FCA78C9E541A26B1459C22684CC0C44906A11C1E0BF0C4FEE0849CFE2D615FA39BBDB10F3900"
#     COURSE_ID = "a9eb1fbf-75b7-4bd4-b88f-e06541a62373"
#     ACAD_YEAR = "2017/2018"
#     SEM = 1
#     SEMESTER_START_DATE = 1502035200
#     a = IVLEScrapper()
#     result = a.get_user_courses(TOKEN)
#     print(result)
#     result = a.get_course_staffs(TOKEN, COURSE_ID)
#     print(result)
#     result = a.get_class_roster(TOKEN, COURSE_ID)
#     print(result)
#     result = a.get_student_groups(TOKEN, COURSE_ID)
#     print(result)

