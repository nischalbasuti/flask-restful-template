# README

## Introduction
Walkthrough to write a super simple CRUD API in python using flask and other tools.

It is assumed that python 3.x, pip and MySQL is installed on your system.

## Getting Started

### Project Structure
```sh
-/
|-app/
||-__init__.py
||-endpoints/ *consists all endpoints, only user endpoint in this project.*
|||-__init__.py
|||-user/
||||-__init__.py
||||-resource.py *consists of routing logic. Similar to controller in rails.*
||||-model.py *consists user model.*
|-env/ *generate with virtualenv.*
|-config.py
|-run.py
```

### Setting up virtualenv (optional)
```sh
pip install virtualenv
```

```sh
virtualenv env
```
#### 'Activating' virtualenv
```sh
source ./env/bin/activate
```
### Installing Flask, Flask-RESTful, Flask-SQLAlchemy and pymysql
```sh
pip install flask
pip install flask-restful
pip install flask-sqlalchemy # ORM, similar to rails active-record.
pip install Flask-Migrate    # Provides rails-like database migration.
pip install pymysql          # python MySQL client.
```

### Initialize Database
```sh
mysql -u <username> -p
```
```sh
mysql> create database demo_app
```

### Set Environment Variables and Run Flask
Set environment variables:
```sh
export FLASK_APP=app.py
export FLASK_DEBUG=true
```
Run flask:
```sh
flask run
```

## Initializing and configuring application.

### Initializing application
In ```app/__init__.py```:

```python
from flask import Flask
app = Flask(__name__)
```

### Configuring application

In ```app/__init__.py```:

```python
...
...
app.config.from_object('config') # load configurations from 'config.py'.
```

In ```config.py```:

```python
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

```

### Create api instance
```python
from flask_restful import Api
api = Api(app)
```

### Database Stuff with SQLAlchemy and Flask-Migrate
First, we make an instance of the database using the application instance.
```python
db = SQLAlchemy(app)
```

Then we have to write a class which represents a row in the database. In this case, a row in the User table.

In ```app/endpoints/user/model.py```

```python
from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    # to get serialized data
    def to_dict(self):
        ret = {c.name: getattr(self, c.name) for c in  self.__table__.columns}
        return ret
```
To generate create and update database tables.
```sh
flask db init # Only needs to be run only the first time. Creates the migrations directory
flask db migrate
flask db upgrade
```

## Handling requests and routing.

```app/endpoints/user/resource.py``` will handle requests.

```python
from flask_restful import Resource, reqparse, abort
from app.endpoints.user import model
from app import db

class User(Resource):

    def get(self, id):
        user = model.User.query.filter_by(id = id).first()
        if user:
            return { "status": "found", "user": user.to_dict() }
        else:
            abort(404, message="user with id %s does not exist" % id)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('name')

        id = parser.parse_args()['id']
        name = parser.parse_args()['name']

        user = model.User(id, name)
        db.session.add(user)
        try:
            db.session.commit()
            return { "status": "saved", "params": user.to_dict() }
        except Exception as e:
            abort(422, message="%s" % str(e))
```

The User resource should then register it's routes in the api.
In ```app/__init__.py```:

```python
from app.endpoints.user.resource import User

api.add_resource(User, '/users/<string:id>', endpoint='get_user')
api.add_resource(User, '/users/', endpoint='create_user')
```

Example request:
```sh
$ curl -X post -H 'Content-Type: application/json' --data '{"id": "1", "name": "nischal"}' localhost:5000/users/

{
    "status": "saved",
    "params": {
        "id": 1,
        "name": "nischal"
    }
}
```

```sh
$ curl -X get localhost:5000/users/1 

{ "status": "found",
    "user": {
        "id": 1,
        "name": "nischal"
    }
}
```
