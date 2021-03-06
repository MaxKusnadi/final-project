from config import DEVELOPMENT
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

API_KEY = "bAbUg4vhpnzADp7DO9GU0"
TEMP_TOKEN = "ACD2D0125D4006AE356EEF14220F0DD529420AB5E3B6C054FCEE296E24B058E98EE8439F4AF920E28A27DA3EA97B0CDEBB179D276D99FE7C8CF33FE5C1181178D6EB87E936DA1A6901585C4A5520E05B6C7F0C9A72CD96E017E62981828FE923BCB7CC3F0F3CBDF25BCD9727DF95DEC6F1630D8C6C0D1879F27B8630447AE208C599CE1826991C8785F0E53FF8B5DD13FD22CEAF401A9DDB612A2C9305A8DDCA6A1C01CD1FB2F1ADA3E440995DD739CE4DC17C40004FE77835DB2367323795D218F09183698224774487B977E148272440FC176B3701B99F383C987FFB4EE697CB7DD13ECFCF8121954C053488C65191"
IVLE_URL = "https://ivle.nus.edu.sg/api/Lapi.svc/"

if DEVELOPMENT:
    redirect_url = "http://localhost"
    LOGIN_REDIRECT_URL_DEV = "http://localhost/login_status"
else:
    redirect_url = "https://imgratefultoday.com"
    LOGIN_REDIRECT_URL_DEV = "http://localhost:3000"
LOGIN_REDIRECT_URL_LIVE = "https://nusattend.tk/"
LOGIN_URL = "https://ivle.nus.edu.sg/api/login/?apikey={api_key}&url={redirect_url}/ivle_token".format(api_key=API_KEY,
                                                                                                       redirect_url=redirect_url)

# LIST OF SERVICE
VALIDATE_URL = "Validate"
PROFILE_URL = "Profile_View"
ACAD_TIME_URL = "MyOrganizer_AcadSemesterInfo"
WEEK_CODE_URL = "CodeTable_WeekTypes"
MODULE_URL = "Modules"
CLASS_ROSTER_URL = "Class_Roster"
STUDENT_GROUP_URL = "Timetable_Student_Module"
LECTURER_URL = "Module_Lecturers"
STAFF_GROUP_URL = "GroupsByUserAndModule"

SESSION = requests.Session()
retries = Retry(total=20,
                backoff_factor=0.5,
                status_forcelist=[500, 502, 503, 504])
SESSION.mount('https://', HTTPAdapter(max_retries=retries))
