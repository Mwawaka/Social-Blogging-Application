from flask import current_app
from app import db, bcrypt
from flask_login import UserMixin
from app import login_manager
import jwt
from datetime import datetime, timedelta

# This sets the callback for reloading a user from the session. The function you set should take a user ID (a str) and return a user object, or None if the user does not exist


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(length=60), nullable=False,
                      unique=True, index=True)
    password_hash = db.Column(db.String(length=128), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    # Password encryption
    @property
    def password(self):
        # Prevent reading password
        raise AttributeError('Password is not readable')
        # return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    # Password verification
    def verify_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)

    # Registration
    # Token authentication using URLSafeTimedSerializer
    # Generates the token

    def generate_confirmation_token(self):
        token = jwt.encode(
            {
                'confirm': self.id,
                'expiration': str(datetime.utcnow() + timedelta(minutes=2))
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    @staticmethod
    def confirm_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        id = payload.get('confirm')
        # returns the user with the id specified in the database
        return User.query.get(id)

    # Token for the new email

    def confirmation_email_token(self, new_email):
        token = jwt.encode(
            {
                'change_email': self.id,
                'email': new_email,
                'expiration': str(datetime.utcnow() + timedelta(minutes=3))
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'

        )
        return token

    @staticmethod
    def confirm_email_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        id = payload.get('change_email')
        email = payload.get('email')
        return (email, User.query.get(id))

    # Token for reset password
    def reset_password_token(self):
        token = jwt.encode(
            {
                'reset': self.id,
                'expiration': str(datetime.utcnow() + timedelta(minutes=3))
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    @staticmethod
    def confirm_reset_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        id = payload.get('reset')
        return User.query.get(id)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    default = db.Column(db.Boolean(), default=False, index=True)
    permissions = db.Column(db.Integer())
    users = db.relationship('User', backref='role', lazy=True)

    # constructor
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # Methods to handle permissions
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles={
            'User':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE],
            'Moderator':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE],
            'Admin':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE,Permission.ADMIN]
        }
        default_role='User'
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()
    def __repr__(self):
        return f'Role {self.name}'
# index-ensures that queries are more efficient
