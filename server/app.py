#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource # type: ignore
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        try:
            json = request.get_json()
            user = User(
                username=json['username'],
                _password_hash=json['password'],
                image_url=json['image_url'],
                bio=json['bio']
            )
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists'}, 422  # Change the status code to 422
        except Exception as e:
            return {'error': str(e)}, 500

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict()
        return {}, 204

class Login(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        user = User.query.filter(User.username == username).first()

        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session['user_id'] = None
            return {}, 204
        return {}, 401

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                recipes = [recipe.to_dict() for recipe in user.recipes]
                return {'recipes': recipes}, 200
        return {}, 401

    def post(self):
        try:
            # Your recipe creation logic here
            return {}, 201
        except ValueError as e:
            return {'error': str(e)}, 422

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)