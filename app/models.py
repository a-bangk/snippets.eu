from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from datetime import datetime, timezone
from . import login
from sqlalchemy.dialects.mysql import INTEGER

class Note(db.Model):
    # Do I need to write db.Integer
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    content = db.Column(db.String(4096))
    entry_datetime = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    update_datetime=db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('user.id'), index=True)
    author = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return '<Note {}>'.format(self.body)

class User(UserMixin, db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(320), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.SmallInteger, default=1)
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