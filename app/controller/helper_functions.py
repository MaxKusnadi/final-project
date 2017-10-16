import requests
import re
from datetime import datetime, timedelta

IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"
API_KEY = "bAbUg4vhpnzADp7DO9GU0"
TOKEN = "36C5E5A0DAEEEFFDE451284055243FD1BAC5B957FD6EF2708290B454946D7B3246D675ECDA538638ECB96E25934984BF8BFEB8AFF005B0A98C959C3D1BA146334AC33453117EF1F69AB5177AEF1EABBB6BAB8D73088FE46CB1D642A8563290866093F1667B6ECB991F3FCCCD54B1E7C08147369D34B1F091D983763C6A0B70FA89B5BA60802F32F86A9485CD655AFFC86081C316699E41271F2634F3FCB0E9CA418450F1BD66C7D0259B8A59FD8F5E364CA9F2CC7C070C2D84B23FFA88BD23BF48B4A4A1271C5430AAE4FCA78C9E541A26B1459C22684CC0C44906A11C1E0BF0C4FEE0849CFE2D615FA39BBDB10F3900"
COURSE_ID = "a9eb1fbf-75b7-4bd4-b88f-e06541a62373"
ACAD_YEAR = "2017/2018"
SEM = 1
SEMESTER_START_DATE = 1502035200

# INPUT: user ivle token
# OUTPUT: list of teaching modules, teaching module is a dictionary with keys: creator_user_id, creator_name, course_id, course_code, course_name, acad_year, semester and permission
def get_teaching_modules(token):
    param = {
        "APIKey": API_KEY,
        "AuthToken": token,
        "Duration": 0,
        "IncludeAllInfo": False
    }
    service = "Modules"
    url = IVLE_URL + service
    resp = requests.get(url, params=param)
    results = resp.json()['Results']
    teaching_modules = filter(lambda x: x['Permission'] != 'S', results)
    return list(map(lambda x: {
        'creator_user_id': x['Creator']['UserID'],
        'creator_name': x['Creator']['Name'],
        'course_id': x['ID'],
        'course_code': x['CourseCode'],
        'course_name': x['CourseName'],
        'acad_year': x['CourseAcadYear'],
        'semester': x['CourseSemester'].split(' ')[-1],
        'permission': x['Permission']
    }, teaching_modules))

# INPUT: user ivle token and course id returned from ivle
# OUTPUT: list of students, student is a dictionary with keys: name, email and matric
def get_class_roster(token, course_id):
    param = {
        "APIKey": API_KEY,
        "AuthToken": token,
        "CourseID": course_id
    }
    service = "Class_Roster"
    url = IVLE_URL + service
    resp = requests.get(url, params=param)
    results = resp.json()['Results']
    return list(map(lambda x: {
        'name': x['Name'],
        'email': x['Email'],
        'matric': x['UserID']
    }, results))


# INPUT: user's ivle token and course id returned from ivle
# OUTPUT: list of groups, group is a dictionary with keys: group_name, start_time, end_time, day_code, week_code, venue, group_type
def get_groups(token, course_id):
    param = {
        "APIKey": API_KEY,
        "AuthToken": token,
        "CourseID": course_id

    }
    service = "Timetable_Module"
    url = IVLE_URL + service
    resp = requests.get(url, params=param)
    results = resp.json()['Results']
    return list(map(lambda x: {
        'group_name': x['ClassNo'],
        'start_time': x['StartTime'],
        'end_time': x['EndTime'],
        'day_code': int(x['DayCode']),
        'week_code': int(x['WeekCode']),
        'venue': x['Venue'],
        'group_type': x['LessonType']
    }, results))

# INPUT: a group as outputted from get_groups, semester_start_date in epoch as stored in DB, semester (int)
# OUTPUT: a list of sessions, a session is a dictionary with keys: week_name, start_date, end_date
def generate_sessions(group, semester_start_date, semester):
    first_monday = get_first_week_monday(datetime.fromtimestamp(semester_start_date), semester)
    start_time, end_time, day_code, week_code = group['start_time'], group['end_time'], group['day_code'], group['week_code']
    start_time_hours, start_time_minutes = int(start_time[:2]), int(start_time[2:])
    end_time_hours, end_time_minutes = int(end_time[:2]), int(end_time[2:])
    week_string = get_week_code_description(week_code)
    week_deltas = convert_week_code_description_to_week_name(week_string)
    days = map(lambda x: (x, first_monday + timedelta(days=day_code-1) + timedelta(weeks=x-1)), week_deltas)
    return list(map(lambda x: {
        'week_name': str(x[0]),
        'start_date': int((x[1] + timedelta(hours=start_time_hours, minutes=start_time_minutes)).timestamp()),
        'end_date': int((x[1] + timedelta(hours=end_time_hours, minutes=end_time_minutes)).timestamp())
    }, days))

# Helper function of generate_sessions
def convert_week_code_description_to_week_name(week_code):
    if week_code == 'EVERY WEEK':
        return [1,2,3,4,5,7,8,9,10,11,12,13,14]
    elif week_code == 'ODD WEEK':
        return [1,3,5,8,10,12]
    elif week_code == 'EVEN WEEK':
        return [2,4,6,9,11,13]
    elif week_code == 'ORIENTATION WEEK':
        return [] #dont care about orientatation week?
    else:
        return list(map(lambda x: (x+1) if x > 6 else x, map(int, week_code.split(','))))

# Helper function of generate_sessions
def get_first_week_monday(semester_start_date, semester):
    if semester == 1:
        return semester_start_date + timedelta(days=7)
    else:
        return semester_start_date

################ CODE NOT NEEDED, get_week_code_description need to be rewrite for actual production code ###################
def get_week_codes():
    param = {
        "APIKey": API_KEY
    }
    service = "CodeTable_WeekTypes"
    url = IVLE_URL + service
    resp = requests.get(url, params=param)
    results = resp.json()['Results']
    # print(list(filter(lambda x: not re.match('^[0-9]+(?:,[0-9]+)*$', x['Description']), results)))
    return dict(list(map(lambda x: [int(x['WeekCode']), x['Description']], results)))

week_codes_map = get_week_codes()

def get_week_code_description(code):
    return week_codes_map[code]
#################

# print(get_teaching_modules(TOKEN))
# print(get_class_roster(TOKEN, COURSE_ID))
group = get_groups(TOKEN, COURSE_ID)[0]
# print(get_week_codes())
# print(convert_week_code_description_to_exact_week_delta('1,2,3,4'))
print(generate_sessions(group, SEMESTER_START_DATE, SEM))
