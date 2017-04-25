import os
import yaml

class Network:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.year_established = None
        self.website = ''
        self.ipv4 = ''
        self.ipv6 = ''
        self.ssl = False
        self.certfp = False
        self.sasl_plain = False
        self.services = ''
        self.services_website = ''

    def __repr__(self):
        return '<Network {}/{}>'.format(self.name, self.ipv4)

    def has_ssl(self):
        return self.ssl

    def has_ipv6(self):
        return self.ipv6


class Networks:
    def __init__(self):
        self.networks = []

    def reload(self):
        self.networks = []
        data = None
        networks_file = os.path.join(os.path.dirname(__file__), '../data/networks.yaml')
        with open(networks_file, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise exc
        for network_iter in data['networks']:
            network = Network(network_iter['name'], network_iter['description'])
            try:
                network.year_established = int(network_iter['year_established'])
            except ValueError:
                pass
            network.website = network_iter['website']
            network.ipv4 = network_iter['ipv4']
            network.ipv6 = network_iter['ipv6']

            network.ssl = network_iter['ssl']
            network.certfp = network_iter['certfp']
            network.sasl_plain = network_iter['sasl_plain']

            network.services = network_iter['services']
            network.services_website = network_iter['services_website']
            self.add_network(network)

    def add_network(self, network):
        if network in self.networks:
            self.networks.remove(network)

        self.networks.append(network)


networks = Networks()
