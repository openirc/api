from itsdangerous import URLSafeTimedSerializer
from flask import current_app


class TokenizerConfigError(Exception):
    def __init__(self, message):
        self.message = message


class Tokenizer:
    def __init__(self, app=None):
        self.key = None
        self.salt = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('TOKENIZER_SECRET_KEY', None)
        app.config.setdefault('TOKENIZER_SECURITY_PASSWORD_SALT', None)

    def try_set(self):
        cfg = current_app.config

        self.key = cfg['TOKENIZER_SECRET_KEY']
        self.salt = cfg['TOKENIZER_SECURITY_PASSWORD_SALT']

        if self.key is None or self.salt is None:
            raise TokenizerConfigError('Tokenizer is not configured.')

    def generate_token(self, data):
        self.try_set()

        serializer = URLSafeTimedSerializer(self.key)
        return serializer.dumps(data, self.salt)

    def confirm_token(self, token, expiration=3600):
        self.try_set()

        serializer = URLSafeTimedSerializer(self.key)
        try:
            data = serializer.loads(
                token,
                salt=self.salt,
                max_age=expiration
            )
        except Exception as e:
            print('couldnt auth: {}'.format(e))
            return None
        return data


tokenizer = Tokenizer()
