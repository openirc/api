import re
from flask import current_app
from flask_restful import Resource, reqparse

from openirc.models import User
from openirc.utils.db import db
from openirc.utils.tokenizer import tokenizer
from openirc.utils.mail import mailer

messages = {
    0: 'You have succesfully registered, you may now sign in.',
    1: 'You have succesfully registered, please verify your email address to sign in.',
    2: 'Password is too short',
    3: 'Email is currently already registered.',
    4: 'Invalid email address',
}


class APISignup(Resource):
    def post(self):
        conf_need_email = current_app.config['EMAIL_VERIFY']

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email you would like to register', required=True)
        parser.add_argument('pass', type=str, help='password used to authenticate', required=True)
        args = parser.parse_args(strict=True)
        email = args['email']
        passwd = args['pass']

        if not re.match(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$', email):
            return {'status': 'err', 'message': messages[4], 'data': 4}

        entry = User.get_by_email(email)
        if entry:
            return {'status': 'err', 'message': messages[3], 'data': 3}

        if len(passwd) < 6:
            return {'status': 'err', 'message': messages[2], 'data': 2}

        user = User(email, passwd)
        opt = 0
        if conf_need_email:
            token = tokenizer.generate_token(user.email)

            mailer.send_signup_confirmation_token(user.email, token)
            extra = 'please verify your email address to sign in.'
            opt = 1
        else:
            user.mark_confirmed()

        db.session.add(user)
        db.session.commit()

        return {'status': 'ok', 'message': messages[opt], 'data': opt}
