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
        # try:
        db.session.commit()
        return { "status": "saved", "params": user.to_dict() }
        # except Exception as e:
        #     abort(422, message="%s" % str(e))

    def put(self):
        pass

    def patch(self):
        pass
        
    def delete(self):
        pass
