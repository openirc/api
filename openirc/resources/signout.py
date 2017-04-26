from flask import request
from flask_login import logout_user
from flask_restful import Resource

from openirc.models import AuthToken
from openirc.utils.db import db
from openirc.resources.decorators import login_required

messages = {
    0: 'You have succesfully logged out',
}


def response(success, i):
    res = 'ok' if success else 'err'
    return {'status': res, 'message': messages[i], 'data': i}


class APISignout(Resource):
    @login_required
    def get(self):
        token = request.headers.get('X-OpenIRC-Auth-Token')

        entry = AuthToken.find_by_token(token)
        assert entry
        AuthToken.query.filter_by(token=token).delete()
        db.session.commit()

        logout_user()

        return response(True, 0)
