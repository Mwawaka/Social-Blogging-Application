import email
from app import db


class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(30),nullable=False,unique=True,index=True)
    email=db.Column(db.String(60),nullable=False,unique=True,index=True)
    password_hash=db.Column(db.String(128),nullable=False)
    role_id=db.Column(db.Integer(),db.ForeignKey('role.id'))

    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    users=db.relationship('User',backref='role',lazy=True)
#index-ensures that queries are more efficient