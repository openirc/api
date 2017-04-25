import re
from flask_restful import Resource, reqparse

from openirc.models import User
from openirc.utils.db import db

messages = {
    0: 'You have succesfully logged in',
    1: 'Password incorrect',
    2: 'Please verify your emaill address before signing in',
    3: 'Email address not registered',
    4: 'Invalid email address',
}


def response(success, i):
    res = 'ok' if success else 'err'
    return {'status': res, 'message': messages[i], 'data': i}

class APISignin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email you would like to register', required=True)
        parser.add_argument('pass', type=str, help='password used to authenticate', required=True)
        args = parser.parse_args(strict=True)
        email = args['email']
        passwd = args['pass']

        if not re.match(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$', email):
            return response(False, 4)

        entry = User.get_by_email(email)
        if not entry:
            return response(False, 3)

        if not entry.is_confirmed():
            return response(False, 2)

        if not entry.check_password(passwd):
            return response(False, 1)

        return response(True, 0)
