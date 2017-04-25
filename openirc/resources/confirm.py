from flask_restful import Resource, reqparse

from openirc.models import User
from openirc.utils.db import db
from openirc.utils.tokenizer import tokenizer

messages = {
    0: 'Email address has been verified, you may now sign in',
    1: 'Email address has already been verified',
    2: 'Confirmation link has expired',
}


def response(success, i):
    res = 'ok' if success else 'err'
    return {'status': res, 'message': messages[i], 'data': i}

class APIConfirm(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, help='token to confirm', required=True)
        args = parser.parse_args(strict=True)
        token = args['token']

        email = tokenizer.confirm_token(token)

        if not email:
            return response(False, 2)

        entry = User.get_by_email(email)
        # ???
        if not entry:
            return response(False, 2)

        if entry.is_confirmed():
            return response(True, 1)
        else:
            entry.mark_confirmed()
            db.session.add(entry)
            db.session.commit()
            return response(True, 0)
