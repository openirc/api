import pytz
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from openirc.utils.db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, db.Sequence('users_user_id_seq'), primary_key=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    pw_hash = db.Column(db.String, default=None)
    tokens = db.relationship('AuthToken', back_populates='user')
    confirmed = db.Column(db.DateTime, default=None)

    def __init__(self, email, password):
        self.set_password(password)
        self.email = email
        self.created = datetime.utcnow()
        self.created = self.created.replace(tzinfo=pytz.UTC)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_confirmed(self):
        return self.confirmed is not None

    def is_anonymous(self):
        return False

    def mark_confirmed(self):
        self.confirmed = datetime.utcnow()
        self.confirmed = self.confirmed.replace(tzinfo=pytz.UTC)

    @classmethod
    def get_by_email(self, email):
        user = User.query.filter_by(email=email).one_or_none()
        return user
