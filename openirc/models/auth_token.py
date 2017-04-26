import pytz
from datetime import datetime

from openirc.utils.db import db


class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'

    token_id = db.Column(db.Integer, db.Sequence('auth_tokens_token_id_seq'), primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), default=None)
    added = db.Column(db.DateTime, nullable=False)
    last_used = db.Column(db.DateTime, nullable=False)
    last_ip = db.Column(db.String, default=None)
    agent = db.Column(db.String, default=None)
    user = db.relationship('User', foreign_keys=[user_id])

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.added = datetime.utcnow()
        self.added = self.added.replace(tzinfo=pytz.UTC)
        self.last_used = self.added

    @classmethod
    def find_by_token(self, token):
        return AuthToken.query.filter_by(token=token).one_or_none()

    @classmethod
    def is_unique(self, token):
        ret = AuthToken.query.filter_by(token=token).count()
        return ret == 0
