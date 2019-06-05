# Create application instance
from flask import Flask
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Database stuff
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db  = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

# Create api instance
from flask_restful import Api
api = Api(app)

# Registering resources.
from app.endpoints.user.resource import User # this class uses app.db, therefore,
                                             # it should be imported after db is
                                             # defined in this file first.

api.add_resource(User, '/users/<string:id>', endpoint='get_user')
api.add_resource(User, '/users/', endpoint='create_user')
