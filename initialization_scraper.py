import requests
from dateutil.parser import parse
from app import db
from app.models.academic_time import AcademicTime

class InitializationScaper:

    @staticmethod
    def initialize():
        ingest_academic_time()

def scrape_academic_weeks():
    IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"
    API_KEY = "bAbUg4vhpnzADp7DO9GU0"
    TOKEN = "CA4D4789F4EB325345562439992BCB0946F0CE922B574795C9BE19C1F0CAEC56A51847029F85A91D834C3CA6C99B1C7FFD3DF01E79811E4451E4561C0DFCE592F1F9DB4F11B0AF9880400942798A3BC6606F533C654990F0CE6DF4A6E0628706C1619B43E595A9BFA103710D46FF8377B87565A5EB51A1BFD47060D7603686F417DAE78615C5301DA600DDE3BAD058A7C6DFEA0764164CA5C7702C2EF66BFF08426965F03C3A2B1B7F143F3AF6004ABD4AD03DAB8B40ED9710B05A37917B3B521069C8858E32E2011F8698BBFBB99D3C32D88504F29AFEDB848A37AD4869FEF41BABC03CA0751CC929EF9634622948B6"

    param = {
        "APIKey": API_KEY,
        "AuthToken": TOKEN,
        "AcadYear": "2017/2018",
        "Semester": 1
    }
    service = "MyOrganizer_AcadSemesterInfo"
    url = IVLE_URL + service
    resp = requests.get(url, params=param)
    return resp.json()['Results']

def date_iso_to_epoch(iso_str):
    iso_str += '+08:00'
    date_time = parse(iso_str)
    return int(date_time.timestamp())

def academic_weeks_to_model_args(raw_json):
    return (
        raw_json['TypeName'],
        raw_json['EvenOddWeek'],
        raw_json['AcadYear'],
        int(raw_json['Semester'].split(' ')[-1]),
        date_iso_to_epoch(raw_json['SemesterStartDate_js']),
        date_iso_to_epoch(raw_json['SemesterEndDate_js'])
    )

def ingest_academic_time():
    response = scrape_academic_weeks()
    for raw_json in response:
        args = academic_weeks_to_model_args(raw_json)
        a = AcademicTime.query.filter(AcademicTime.acad_year == args[2],
                                      AcademicTime.semester == args[3],
                                      AcademicTime.week_name == args[0]
                                      ).first()
        if not a:
            academic_time = AcademicTime(*args)
            db.session.add(academic_time)
    db.session.commit()

def print_db():
    a = AcademicTime.query.all()
    print(len(a))
    print(a[0])

if __name__ == "__main__":
    InitializationScaper.initialize()
    print_db()
