import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
login_manager = LoginManager(app)
db = SQLAlchemy(app)

# Models
from app.models.user import User

# Views
from app.views.login import *
