# OpenIRC API
This is the API Account Endpoint for OpenIRC.

## Requirements
* `pip install -r requirements.txt`

## Installation

* `git clone https://github.com/openirc/api.git`
* Copy and modify the contents of `openirc/defaults.cfg` to your liking.

### Setting up the database:
* `sudo su postgres`
* If current user has no PostgreSQL account (invalid role), `createuser <user>`
* `createdb -O <user> openirc`
* `exit` (back to your user)
* `flask db upgrade`


## Running
* `FLASK_APP=openirc/app.py FLASK_DEBUG=0 OPENIRC_CONFIG=path/to/openirc.cfg`
* `flask run --host=0.0.0.0`
