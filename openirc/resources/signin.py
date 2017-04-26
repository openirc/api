import random
import re
import string
from flask import request
from flask_login import current_user
from flask_restful import Resource, reqparse

from openirc.models import AuthToken, User
from openirc.utils.db import db

messages = {
    0: 'You have succesfully logged in',
    1: 'Password incorrect',
    2: 'Please verify your emaill address before signing in',
    3: 'Email address not registered',
    4: 'Invalid email address',
    5: 'You are already logged in',
}


def response(success, i):
    res = 'ok' if success else 'err'
    code = 200 if success else 401
    return {'status': res, 'message': messages[i], 'data': i}, code

def randtoken(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


class APISignin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email you would like to register', required=True)
        parser.add_argument('pass', type=str, help='password used to authenticate', required=True)
        args = parser.parse_args(strict=True)
        email = args['email']
        passwd = args['pass']

        if current_user and current_user.is_authenticated:
            return response(False, 5)

        if not re.match(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$', email):
            return response(False, 4)

        user = User.get_by_email(email)
        if not user:
            return response(False, 3)

        if not user.is_confirmed():
            return response(False, 2)

        if not user.check_password(passwd):
            return response(False, 1)

        token = randtoken(50)
        while not AuthToken.is_unique(token):
            token = randtoken(50)

        token_entry = AuthToken(token, user.user_id)

        ip = '255.255.255.255'
        if len(request.access_route):
            ip = request.access_route[0]

        token_entry.last_ip = ip
        token_entry.agent = request.headers.get('User-Agent')

        db.session.add(token_entry)
        db.session.commit()

        return {'status': 'ok', 'message': messages[0], 'data': 0, 'token': token}
