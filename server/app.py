#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password'] 
        if username and password:
            user = User(
                username=username
            )
            user.password_hash = password
            db.session.add(user)
            db.session.commit()

            session['user_id']= user.id
            return user.to_dict(), 201
        return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):
    def get(self):
        user = User.query.filter_by(id=session['user_id']).first()
        if user:
            return user.to_dict()
        return make_response({}, 204)

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.username == data['username']).first()
        if user and user.authenticate(data['password']):
            return make_response(user.to_dict(), 200)
        return make_response({}, 404)
            


class Logout(Resource):
    def delete(self):
        session['user_id'] = None

        return make_response({}, 205)

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear', endpoint='clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
