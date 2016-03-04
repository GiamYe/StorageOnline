__author__ = 'zhenanye'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from db import db_session
Base = declarative_base()
SECRET_KEY = 'whats fucking the yunpan'

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    ctime = Column(DateTime)
    utime = Column(DateTime)
    child_ms = relationship("Membership", cascade="all,delete", backref="user")
    child_folder = relationship("Folder", cascade="all,delete", backref="user")
    child_file = relationship("File", cascade="all,delete", backref="user")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    def verify_password(self, password):
        return self.password == password

    def generate_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = db_session.query(User).filter_by(id=data['id']).first()
        return user

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ctime = Column(DateTime)
    utime = Column(DateTime)
    child = relationship("Membership", cascade="all,delete",  backref="group")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Membership(Base):
    __tablename__ = 'membership'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    group_id = Column(ForeignKey('group.id', ondelete='CASCADE'))
    ctime = Column(DateTime)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'group_id': self.group_id,
        }


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    parent_id = Column(Integer)
    path = Column(String(5000))
    name = Column(String(50))
    deleted = Column(Boolean)
    ctime = Column(DateTime)
    utime = Column(DateTime)
    child = relationship("File", cascade="all,delete",  backref="folder")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'path': self.path,
            'parent_id': self.parent_id,
            'ctime': self.ctime,
        }


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    folder_id = Column(ForeignKey('folder.id', ondelete='CASCADE'))
    name = Column(String(50))
    location = Column(String(5000))
    type = Column(String(50))
    deleted = Column(Boolean)
    ctime = Column(DateTime)
    utime = Column(DateTime)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'folder_id': self.folder_id,
            'user_id': self.user_id,
            'ctime': self.ctime,
        }


class Shared(Base):
    __tablename__ = 'shared'
    id = Column(Integer, primary_key=True)
    from_user_id = Column(ForeignKey('user.id'))
    to_user_id = Column(ForeignKey('user.id'))
    to_group_id = Column(ForeignKey('group.id'))
    folder_id = Column(ForeignKey('folder.id'))
    file_id = Column(ForeignKey('file.id'))
    privilege = Column(String(50))
    ctime = Column(DateTime)
    utime = Column(DateTime)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'from': self.from_user_id,
            'to_user': self.to_user_id,
            'to_group': self.to_group_id,
            'folder_id': self.folder_id,
            'file_id': self.file_id,
            'privilege': self.privilege,
        }