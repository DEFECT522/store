# pythonic/models.py
from pythonic import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    requests = db.relationship("Request", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(125), unique=True, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.created_at + timedelta(minutes=10)



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    devices = db.relationship("Device", backref="category", lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    devices = db.relationship("Device", backref="type", lazy=True)
    def __repr__(self):
        return f"Type('{self.name}')"


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.String(60), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)

    def __repr__(self):
        return f"Device('{self.name}', '{self.price}')"


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship("Device")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Request('{self.device.name}', '{self.user.username}', '{self.created_at}')"


class DoneRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    request = db.relationship("Request")
    done_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"DoneRequest('{self.request.device.name}', '{self.done_at}')"

