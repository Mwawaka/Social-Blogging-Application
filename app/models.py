from email.policy import default
from app import db,bcrypt
from flask_login import UserMixin
from app import login_manager
from flask import current_app



# This sets the callback for reloading a user from the session. The function you set should take a user ID (a str) and return a user object, or None if the user does not exist
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(length=128), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    confirmed=db.Column(db.Boolean(),default=False)
    
    #Password encryption
    @property
    def password(self):
        #Prevent reading password
        raise AttributeError('Password is not readable')
        # return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    # Password verification
    def verify_password(self,login_password):
        return bcrypt.check_password_hash(self.password_hash,login_password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'Role {self.name}'
# index-ensures that queries are more efficient
