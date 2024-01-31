from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, SmallInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'
    ID = Column(Integer, primary_key=True)
    STREET = Column(VARCHAR(128))
    CODE = Column(VARCHAR(128))
    TOWN = Column(VARCHAR(128))
    REGION = Column(VARCHAR(128))
    tag_id = Column(Integer, ForeignKey('notetag.id'))
    country_id = Column(SmallInteger, ForeignKey('country.id'))

class Associate_Notetag_Note(Base):
    __tablename__ = 'associate_notetag_note'
    notetag_id = Column(Integer, ForeignKey('notetag.id'), primary_key=True)
    note_id = Column(Integer, ForeignKey('note.id'), primary_key=True)

class Associate_Source_Author(Base):
    __tablename__ = 'associate_source_author'
    source_id = Column(Integer, ForeignKey('source.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True)

class Associate_Source_Note(Base):
    __tablename__ = 'associate_source_note'
    source_id = Column(Integer, ForeignKey('source.id'), primary_key=True)
    note_id = Column(Integer, ForeignKey('note.id'), primary_key=True)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    forename = Column(VARCHAR(128))
    surname = Column(VARCHAR(128))
    title = Column(VARCHAR(128))
    middlename = Column(VARCHAR(256))
    postnominal = Column(VARCHAR(32))
    birthyear = Column(VARCHAR(16))
    deathyear = Column(VARCHAR(16))
    full_name = Column(VARCHAR(512))
    comment = Column(VARCHAR(1024))

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    English_name = Column(VARCHAR(512))
    iso_code = Column(VARCHAR(2))

class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    genre = Column(VARCHAR(50))

class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    content = Column(VARCHAR(4096))
    entry_datetime = Column(DateTime)
    update_datetime = Column(DateTime)
    object_type_id = Column(SmallInteger, ForeignKey('object_type.id'))
    temp_source = Column(VARCHAR(512))
    url_source = Column(VARCHAR(512))

class Notetag(Base):
    __tablename__ = 'notetag'
    id = Column(Integer, primary_key=True)
    tag = Column(VARCHAR(512))
    entry_datetime = Column(DateTime)
    update_datetime = Column(DateTime)

class Object_Type(Base):
    __tablename__ = 'object_type'
    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(128))

class Source(Base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    entry_datetime = Column(DateTime)
    update_datetime = Column(DateTime)
    source_type_id = Column(Integer, ForeignKey('source_type.id'))
    title = Column(VARCHAR(256))
    year = Column(SmallInteger)
    url = Column(VARCHAR(512))

class Source_Type(Base):
    __tablename__ = 'source_type'
    id = Column(Integer, primary_key=True)
    entry = Column(VARCHAR(100))

class User(UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password_hash = Column(VARCHAR(512))
    active = Column(Boolean)
    created = Column(DateTime)
    updated = Column(DateTime)
