import hashlib
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False, index=True)
    role = db.Column(db.Integer, nullable=False, index=True)

    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
