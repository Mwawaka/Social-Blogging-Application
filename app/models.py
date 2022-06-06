from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(60), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

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
