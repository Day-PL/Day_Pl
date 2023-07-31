from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    def __init__(self):
        self.pwd_hash = None

    id         = db.Column(db.String(128), primary_key = True)
    _id        = db.Column(db.String(64), unique = True, nullable = False)
    pwd_hash   = db.Column(db.String(128),               nullable = False)
    name       = db.Column(db.String(64),                nullable = False)
    gender     = db.Column(db.String(64),                nullable = False)
    birthdate  = db.Column(db.DateTime,                  nullable = False)
    phone      = db.Column(db.String(32), unique = True, nullable = False)
    mail       = db.Column(db.String(32), unique = True, nullable = False)
    rq_terms   = db.Column(db.Boolean,                   nullable = False)
    op_terms   = db.Column(db.Boolean,                   nullable = False)
    sign_date  = db.Column(db.DateTime,                  nullable = False)

    def set_pwd(self, password):
        self.pwd_hash = generate_password_hash(password)
    def check_pwd(self, password):
        return check_password_hash(self.pwd_hash, password)
    