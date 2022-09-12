from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from lmdb import Environment
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  
from os import getenv

appl = Flask(__name__)
CORS(appl)
appl.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tracker.db'
appl.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET")


jwt = JWTManager(appl)
db = SQLAlchemy(appl)
logdb = Environment("../tracker_log.db")
migrate = Migrate(appl, db)
API_PREFIX = '/api/v1/'

