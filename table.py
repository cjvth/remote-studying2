import datetime

from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    creator_id = db.Column(db.Integer,)
    users = orm.relation("User", back_populates='group')
    teachers = orm.relation("Teacher", back_populates='group')
    lessons = orm.relation("Lesson", back_populates='group')
    subgroups = orm.relation("Subgroup", back_populates='group')
    chats = orm.relation("Chat", back_populates='group')


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = orm.relation('Group')
    name = db.Column(db.String, nullable=False)
    access = db.Column(db.Integer, default=0, nullable=False)
    hashed_password = db.Column(db.String, index=True)
    password_time = db.Column(db.DateTime)
    subgroups = orm.relation("Subgroup", secondary="user_subgroup", backref="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        self.password_time = datetime.datetime.now() + datetime.timedelta(days=1)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = orm.relation('Group')
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    lessons = orm.relation('Lesson', back_populates='teacher')


class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), index=True, nullable=False)
    group = orm.relation('Group')
    subgroup_id = db.Column(db.Integer, db.ForeignKey("subgroups.id"), default=0, nullable=False)
    subgroup = orm.relation('Subgroup')
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = orm.relation('Teacher')
    title = db.Column(db.String, nullable=False)
    names = db.Column(db.String)
    zoom_login = db.Column(db.Integer)
    zoom_password = db.Column(db.Integer)
    info = db.Column(db.String)
    homework = db.Column(db.String)


class Subgroup(db.Model):
    __tablename__ = "subgroups"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = orm.relation('Group')
    name = db.Column(db.String, nullable=False)
    users = orm.relation("User", secondary="user_subgroup", backref="subgroup")


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = orm.relation('Group')


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)


user_subgroup = db.Table('user_subgroup', db.metadata,
                         db.Column('user', db.Integer, db.ForeignKey('users.id'), nullable=False),
                         db.Column('subgroup', db.Integer, db.ForeignKey('subgroups.id'), nullable=False))

if __name__ == '__main__':
    db.create_all()
