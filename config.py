from app import app

DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application configurations for SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/demo_app'

DATABASE_CONNECT_OPTIONS = {
        "SQLALCHEMY_ECHO"                : True,
        "SQLALCHEMY_TRACK_MODIFICATIONS" : False,
        }


