from app import app, db, api, login_manager
from .models import User
from datetime import datetime
from flask import request, jsonify, abort
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_login import login_user, current_user, logout_user
from urllib.parse import urlparse, urljoin
from .parsers import *


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def check_perm(fun):
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return fun(*args, **kwargs)
        return "No permission", 403
    return wrap


def private_permission(cls):
    methods = ('get', 'post', 'patch', 'delete')
    callable_attributes = {k: cls.__dict__[k] for k in methods if cls.__dict__.get(k)}
    for name, func in callable_attributes.items():
        decorated = check_perm(func)
        setattr(cls, name, decorated)
    return cls


@private_permission
@api.resource('/private/users')
class UsersPrivate(Resource):

    def get(self):
        users = User.query.all()
        return {_.id: _.private_serialize for _ in users}, 200


@private_permission
@api.resource('/private/user/<int:id>', '/private/user')
class UsersPrivateDetail(Resource):

    def get(self, id):
        user = User.query.get(id)
        if user:
            return user.private_serialize, 200
        return "Wrong user", 404

    def post(self):
        user = User.query.filter_by(email=post_parser.parse_args()['email']).first()
        if user:
            return "User with with this email already exist", 404
        new_user = User(**private_user_parser.parse_args())
        db.session.add(new_user)
        db.session.commit()
        return f'new user {new_user}', 200

    def patch(self, id):
        user = User.query.get(id)
        if user:
            parser = private_user_parser.parse_args()
            for atr, val in parser.items():
                if val:
                    setattr(user, atr, val)
            db.session.commit()
            return user.private_serialize, 200
        return {'message': 'User don`t exist'}, 400

    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f'User {user.last_name} was deleted'
        return {'wrong user'}, 404


@api.resource('/login', '/logout')
class LogInOut(Resource):

    def get(self):
        logout_user()
        return "Logout", 200

    def post(self):
        email = login_parser.parse_args().get('email')
        password = login_parser.parse_args().get('password')
        user = User.query.filter_by(email=email).first()
        print(user)
        if user is None:
            return 'wrong email', 400
        if not user.check_password(password):
            print('wrong password')
            return 'wrong email or password', 400
        login_user(user, remember=True)
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        print(current_user.is_authenticated)
        print(current_user.is_authenticated)
        return 'Logged in successfully.', 200


@api.resource('/users')
class Users(Resource):

    def get(self):
        users = User.query.all()
        return {_.id: _.base_serialize for _ in users}, 200


@api.resource('/user/<int:id>')
class OneUser(Resource):

    def get(self, id):
        return User.query.get(id).base_serialize, 200


@api.resource('/makeuser')
class MakeUser(Resource):

    def post(self):
        post_parser.parse_args()['is_admin'] = True
        secret_key = request.args.get('secret_key')
        user = User.query.filter_by(email=post_parser.parse_args()['email']).first()
        if user:
            return "User with with this email already exist", 404
        if secret_key == app.config['SECRET_KEY']:
            new_user = User(**post_parser.parse_args(), is_admin=True)
        else:
            new_user = User(**post_parser.parse_args())
        db.session.add(new_user)
        db.session.commit()
        return f'new user {new_user}', 200


@api.resource('/users/current')
class Me(Resource):

    def get(self):
        if current_user.is_authenticated:
            return f'Hello {current_user.first_name}', 200
        return 'Please login', 401

    def patch(self):
        if current_user.is_authenticated:
            me = current_user
            parser = private_user_parser.parse_args()
            for atr, val in parser.items():
                if val:
                    setattr(me, atr, val)
            db.session.commit()
            return f'Hello {current_user.first_name}', 200
        return 'Please login', 401
