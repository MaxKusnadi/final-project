import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
import flask_excel as excel

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

# CREATING LOGGER
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


app = Flask(__name__, static_url_path="")
CORS(app, supports_credentials=True)
app.config.from_object('config')
socketio = SocketIO(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
excel.init_excel(app)

# Models
from app.models.user import User
from app.models.academic_time import AcademicTime
from app.models.attendance import Attendance
from app.models.course import Course, CourseStaff, CourseStudent
from app.models.group import Group, GroupStaff, GroupStudent
from app.models.session import Session
from app.models.week_code import WeekCode

# Views
from app.views.login import *
from app.views.academic_time import *
from app.views.mock.user import *
from app.views.mock.login import *
from app.views.mock.course import *
from app.views.mock.session import *
from app.views.mock.group import *
from app.views.user import *
from app.views.course import *
from app.views.group import *
from app.views.session import *
from app.views.attendance import *

