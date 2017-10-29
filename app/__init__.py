import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO

logging.getLogger('socketio').setLevel(logging.CRITICAL)
logging.getLogger('engineio').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
socketio = SocketIO(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

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

