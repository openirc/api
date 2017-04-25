import time
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api

from openirc.utils.config import init_config
from openirc.utils.db import db
from openirc.utils.mail import mail, mailer
from openirc.utils.tokenizer import tokenizer
from openirc.utils.networks import networks
from openirc.models.auth_token import AuthToken
from openirc.resources import *


app = Flask('openirc')
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

init_config(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail.init_app(app)
mailer.init_app(mail, app.config['WEB_LINK'])
tokenizer.init_app(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

migrate = Migrate(app, db)

networks.reload()

prefix = '/api/v1'

api.add_resource(APINetworks, '{}/networks'.format(prefix))
api.add_resource(APISignup, '{}/signup'.format(prefix))
api.add_resource(APISignin, '{}/signin'.format(prefix))
api.add_resource(APIConfirm, '{}/confirm'.format(prefix))

@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('X-OpenIRC-Auth-Token')
    if not token:
        return None

    token_data = AuthToken.find_by_token(token)
    if not token_data:
        return None

    assert token_data.user
    return token_data.user
