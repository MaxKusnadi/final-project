from app.models.week_code import WeekCode


class Utils:

    @staticmethod
    def create_error_code(error, *args):
        d = error
        d['text'] = d['text'].format(args)
        return d

    @staticmethod
    def get_course_info(course):
        d = dict()
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
        d['metric'] = user.metric
        d['email'] = user.email
        return d

    @staticmethod
    def get_group_info(group):
        d = dict()
        d['group_name'] = group.group_name
        d['course_code'] = group.course.course_code
        d['start_time'] = group.start_time
        d['end_time'] = group.end_time
        d['day_code'] = group.day_code
        d['week_code'] = WeekCode.query.filter(WeekCode.week_code == group.week_code).first().description
        d['venue'] = group.venue
        d['group_type'] = group.group_type
        return d
