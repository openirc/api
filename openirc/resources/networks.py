import json
from flask_restful import Resource

from openirc.utils.networks import networks


class APINetworks(Resource):
    def get(self):
        return json.dumps([network.__dict__ for network in networks.networks])
