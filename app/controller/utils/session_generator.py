import logging

from datetime import datetime, timedelta
from app.models.week_code import WeekCode

SEMESTER_START_DATE = 1502035200
SEMESTER = 1


class SessionGenerator:

    def generate_sessions(self, group):
        logging.info("Generating sessions for group {}".format(group.id))
        first_monday = self._get_first_week_monday(datetime.fromtimestamp(SEMESTER_START_DATE), SEMESTER)
        start_time, end_time, day_code, week_code = group.start_time, group.end_time, group.day_code, group.week_code
        if day_code == -1 or week_code == -1:
            return list()
        start_time_hours, start_time_minutes = int(start_time[:2]), int(start_time[2:])
        end_time_hours, end_time_minutes = int(end_time[:2]), int(end_time[2:])
        week_string = self._get_week_code_description(week_code)
        week_deltas = self._convert_week_code_description_to_week_name(week_string)
        days = map(lambda x: (x, first_monday + timedelta(days=day_code - 1) + timedelta(weeks=x - 1)), week_deltas)
        return list(map(lambda x: {
            'week_name': str(x[0] if x[0] < 7 else x[0] - 1),
            'start_date': int((x[1] + timedelta(hours=start_time_hours, minutes=start_time_minutes)).timestamp()),
            'end_date': int((x[1] + timedelta(hours=end_time_hours, minutes=end_time_minutes)).timestamp())
        }, days))

    # Helper function of generate_sessions
    def _convert_week_code_description_to_week_name(self, week_code):
        if week_code == 'EVERY WEEK':
            return [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14]
        elif week_code == 'ODD WEEK':
            return [1, 3, 5, 8, 10, 12, 14]
        elif week_code == 'EVEN WEEK':
            return [2, 4, 6, 9, 11, 13]
        elif week_code == 'ORIENTATION WEEK':
            return []
        else:
            return list(map(lambda x: (x + 1) if x > 6 else x, map(int, week_code.split(','))))

    # Helper function of generate_sessions
    def _get_first_week_monday(self, semester_start_date, semester):
        if semester == 1:
            return semester_start_date + timedelta(days=7)
        else:
            return semester_start_date

    def _get_week_code_description(self, code):
        week_code = WeekCode.query.filter(WeekCode.week_code == code).first()
        return week_code.description
