from app.models.academic_time import AcademicTime


class Utils:

    @staticmethod
    def create_error_code(error, *args):
        d = error
        d['text'] = d['text'].format(*args)
        return d

    @staticmethod
    def get_course_info(course):
        d = dict()
        d['course_id'] = course.id
        d['creator_name'] = course.creator_name
        d['course_code'] = course.course_code
        d['course_name'] = course.course_name
        d['acad_year'] = course.acad_year
        d['semester'] = course.semester
        return d

    @staticmethod
    def get_user_info(user):
        d = dict()
        d['name'] = user.name
        d['matric'] = user.matric
        d['email'] = user.email
        return d

    @staticmethod
    def get_group_info(group):
        d = dict()
        d['group_id'] = group.id
        d['group_name'] = group.group_name
        d['course_code'] = group.course.course_code
        d['start_time'] = group.start_time
        d['end_time'] = group.end_time
        d['day_code'] = group.day_code
        d['week_code'] = group.week_code
        d['venue'] = group.venue
        d['group_type'] = group.group_type
        d['course_id'] = group.course.id
        d['course_name'] = group.course.course_name
        return d

    @staticmethod
    def get_session_info(session):
        d = dict()
        d['session_id'] = session.id
        d['group_name'] = session.group.group_name
        d['course_code'] = session.group.course.course_code
        d['start_date'] = session.start_date
        d['end_date'] = session.end_date
        d['is_code_generated'] = True if session.code else False
        d['attendance_closed_time'] = session.attendance_closed_time
        d['start_time'] = session.group.start_time
        d['end_time'] = session.group.end_time
        d['venue'] = session.group.venue
        d['group_type'] = session.group.group_type
        d['day_code'] = session.group.day_code
        return d

    @staticmethod
    def get_week_name(now_time):
        # Getting academic time information
        academic_week = AcademicTime.query.filter(AcademicTime.start_date <= now_time,
                                                  AcademicTime.end_date >= now_time).first()
        d = dict()
        if academic_week:
            d['week_name'] = academic_week.week_name
            d['even_odd_week'] = academic_week.even_odd_week
            d['acad_year'] = academic_week.acad_year
            d['semester'] = academic_week.semester
            d['start_date'] = academic_week.start_date
            d['end_date'] = academic_week.end_date
            d['status'] = 200
            return d

        # Check if it's weekend
        academic_week = AcademicTime.query.filter(AcademicTime.end_date >= now_time).first()
        if academic_week:
            d['week_name'] = academic_week.week_name
            d['even_odd_week'] = academic_week.even_odd_week
            d['acad_year'] = academic_week.acad_year
            d['semester'] = academic_week.semester
            d['start_date'] = academic_week.start_date
            d['end_date'] = academic_week.end_date
            d['status'] = 200
            return d

    @staticmethod
    def get_attendance_info(attendance):
        d = dict()
        d['status'] = attendance.status
        d['remark'] = attendance.remark
        d['name'] = attendance.user.name
        d['matric'] = attendance.user.matric
        d['email'] = attendance.user.email
        return d

    @staticmethod
    def get_missing_attendance_info(user):
        d = dict()
        d['status'] = 0
        d['remark'] = ""
        d['name'] = user.name
        d['matric'] = user.matric
        d['email'] = user.email
        return d
