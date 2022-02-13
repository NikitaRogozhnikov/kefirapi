from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    other_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    birthday = db.Column(db.Date)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    city = db.Column(db.String(120), db.ForeignKey('cities.city_name'))

    def __init__(self, first_name, last_name, password,
                 other_name=None, email=None, phone=None,
                 birthday=None, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.is_admin = is_admin
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def base_serialize(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'city': self.city}

    @property
    def private_serialize(self):
        return {'first_name': self.first_name,'last_name': self.last_name,
                'is_admin': self.is_admin, 'other_name': self.other_name,
                'email': self.email, self.phone: 'phone', 'birthday': self.birthday, 'city': self.city}

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.last_name)


class City(db.Model):
    __tablename__ = 'cities'

    # city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(120), primary_key=True)
    users = db.relationship('User', backref='cities', lazy=True)

    def __init__(self,city):
        self.city = city

    def __repr__(self):
        return self.city

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
