from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, SmallInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from datetime import datetime, timezone
from . import login

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    entry_datetime = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    update_datetime=db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    #object_type_id = db.relationship('Object_Type', back_populates='type')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    author = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return '<Note {}>'.format(self.body)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Integer)
    created = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    notes = db.relationship('Note', back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))