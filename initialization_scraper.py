import requests

from dateutil.parser import parse
from app import db
from app.models.academic_time import AcademicTime
from app.constants.ivle import IVLE_URL, ACAD_TIME_URL, API_KEY, TEMP_TOKEN


class InitializationScraper:

    def initialize(self):
        self._ingest_academic_time()

    def _scrape_academic_weeks(self):
        url = IVLE_URL + ACAD_TIME_URL
        params = {
            "APIKey": API_KEY,
            "AuthToken": TEMP_TOKEN,
            "AcadYear": "2017/2018",
            "Semester": 1
        }
        resp = requests.get(url, params=params)
        return resp.json()['Results']

    def _date_iso_to_epoch(self, iso_str):
        iso_str += '+08:00'
        date_time = parse(iso_str)
        return int(date_time.timestamp())

    def _academic_weeks_to_model_args(self, raw_json):
        return (
            raw_json['TypeName'],
            raw_json['EvenOddWeek'],
            raw_json['AcadYear'],
            int(raw_json['Semester'].split(' ')[-1]),
            self._date_iso_to_epoch(raw_json['SemesterStartDate_js']),
            self._date_iso_to_epoch(raw_json['SemesterEndDate_js'])
        )

    def _ingest_academic_time(self):
        response = self._scrape_academic_weeks()
        for raw_json in response:
            args = self._academic_weeks_to_model_args(raw_json)
            a = AcademicTime.query.filter(AcademicTime.acad_year == args[2],
                                          AcademicTime.semester == args[3],
                                          AcademicTime.week_name == args[0]
                                          ).first()
            if not a:
                academic_time = AcademicTime(*args)
                db.session.add(academic_time)
        db.session.commit()


if __name__ == "__main__":
    initial = InitializationScraper()
    initial.initialize()
