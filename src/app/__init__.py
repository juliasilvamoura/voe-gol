import os
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

DB = SQLAlchemy()

def creat_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{USER_DB}:{PASSWORD_DB}@postgres:5432/{NAME_DB}"
    DB.init_app(app)

    return app