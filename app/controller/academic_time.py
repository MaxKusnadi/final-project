import logging

from datetime import datetime
from app.constants.time import TIMEZONE
from app.models.academic_time import AcademicTime


class AcademicTimeController:

    def get_acad_time(self):
        logging.info("Getting current academic time")
        now = datetime.now(TIMEZONE)
        logging.info("Current time: {}".format(now))
        now_epoch = int(now.timestamp())
        logging.info("Current time in epoch: {}".format(now_epoch))

        # Getting academic time information
        academic_week = AcademicTime.query.filter(AcademicTime.start_date <= now_epoch,
                                                  AcademicTime.end_date >= now_epoch).first()
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
        academic_week = AcademicTime.query.filter(AcademicTime.end_date >= now_epoch).first()
        if academic_week:
            d['week_name'] = academic_week.week_name
            d['even_odd_week'] = academic_week.even_odd_week
            d['acad_year'] = academic_week.acad_year
            d['semester'] = academic_week.semester
            d['start_date'] = academic_week.start_date
            d['end_date'] = academic_week.end_date
            d['status'] = 200
            return d
        d['text'] = "Academic time is not found. Please contact support"
        d['status'] = 404
        return d
