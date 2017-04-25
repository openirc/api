from datetime import datetime

from openirc.utils.db import db


class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'

    token_id = db.Column(db.Integer, db.Sequence('auth_tokens_token_id_seq'), primary_key=True, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), default=None)
    added = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

    @classmethod
    def find_by_token(self, token):
        return AuthToken.query.filter_by(token=token).one_or_none()

    @classmethod
    def is_unique(self, token):
        ret = AuthToken.query.filter_by(token=token).count()
        return ret == 0
