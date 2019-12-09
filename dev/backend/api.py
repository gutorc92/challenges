"""
Root file to EduQC's API

The resoucers available should be defined into settings.py
"""

from os import environ
import argparse
from datetime import datetime
import re
import json
import logging
from functools import wraps
import traceback
from dotenv import load_dotenv, find_dotenv
from eve import Eve
from eve.auth import BasicAuth, requires_auth
from eve.io.mongo import MongoJSONEncoder
from eve_healthcheck import EveHealthCheck
from flask import request, abort, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from bson.objectid import ObjectId
from utils import RedisCache, insert_basic_data
from gr_auth import GrAuth

# pylint: disable=ungrouped-imports
# pylint: enable=ungrouped-imports
# import ipdb
# pylint: disable=unused-import
try:
    load_dotenv(find_dotenv())
except IOError as exception:
    pass

# pylint: disable=too-many-arguments
class MyBasicAuth(BasicAuth):
    """ Module to validate the auth user to access the API data"""

    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        return username == environ.get("MONGO_USER") and password == environ.get("MONGO_PASS")
# pylint: enable=too-many-arguments

# pylint: disable=method-hidden
class JSONEncoder(json.JSONEncoder):
    """ class to enconde json with bson and datetime """

    def default(self, o):
        """
            parse objet to json
        """
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
# pylint: enable=method-hidden

# pylint: disable=invalid-name
app = Eve()
app.logger.setLevel(logging.INFO)
app.name = 'API'
app.json_encoder = MongoJSONEncoder
CORS(app)
BCRYPT = Bcrypt(app)
app.__bcrypt__ = BCRYPT
USER_HOST = environ.get("MONGO_HOST_USER", 'users')
EveHealthCheck(app, '/healthcheck')
RedisCache(app, host=environ.get("REDIS", 'redis'))
app.gr_auth = GrAuth(app)

p = argparse.ArgumentParser()

p.add_argument('-b', '--basic-data', help='Apenas insere dados', action='store_true')
#pylint: enable=invalid-name

@requires_auth('home')
def before_insert(documents):
    """Generate a hash for each user document on insert using bcrypt"""
    # argumentos = request.args.to_dict()
    # contests = contests.find({'platform': })
    for doc in documents:
        if ('auth' in doc and
                'password' in doc['auth']):
            doc['auth']['password'] = BCRYPT.generate_password_hash(
                doc['auth']['password']).decode()
        elif ('auth' in doc and
              ('googleHash' in doc['auth'] or
               'facebookHash' in doc['auth'])):
            continue
        else:
            abort(422, description='Auth incorrect, requires at least one field')

@requires_auth('home')
# pylint: disable=unused-argument
def before_update(updates, original):
    """Generate a hash for user changing password on insert using bcrypt"""
    try:
        updates['auth'].pop('password')
    except KeyError:
        pass
    if 'pswdtk' in request.headers:
        new_password = request.headers['pswdtk']
        if 'email' in updates:
            app.data.pymongo().db.users.update({'email': updates['email']}, {
                "$set": {"auth.password": BCRYPT.generate_password_hash(
                    new_password).decode()}}, upsert=True)
            user = app.data.pymongo().db.users.find_one({'email': updates['email']})
        else:
            app.data.pymongo().db.users.update({'_id': original['_id']}, {
                "$set": {"auth.password": BCRYPT.generate_password_hash(
                    new_password).decode()}}, upsert=True)
            user = app.data.pymongo().db.users.find_one({'_id':original['_id']})
        updates['auth'] = user['auth']
        # import ipdb; ipdb.set_trace()
        return
# pylint: enable=unused-argument

# pylint: disable=broad-except
@app.route('/user/auth', methods=['POST'])
def authenticate():
    """ Authenticate user or add social hash """
    try:
        result = app.gr_auth.authenticate()
        return jsonify(result)
    except Exception as error:
        print(traceback.format_exc())
        abort(401, description=str(error))
# pylint: enable=broad-except

# pylint: disable=invalid-name
def auth_resource(resource):
    """ Auth resource """
    def fdec(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(resource=resource, *args, **kwargs)
        return wrapped
    return fdec
# pylint: enable=invalid-name

# pylint: disable=unused-argument
# pylint: disable=broad-except
@app.route('/user/logout', methods=['POST'])
@auth_resource('user_login')
@requires_auth('resource')
def logout(*args, **kwargs):
    """ Authenticate user or add social hash """
    try:
        result = app.gr_auth.logout()
        return jsonify(result)
    except Exception as error:
        print(traceback.format_exc())
        abort(401, description=str(error))
# pylint: enable=broad-except
# pylint: enable=unused-argument

@requires_auth('home')
# pylint: disable=broad-except
# pylint: disable=unused-argument
def fetched_users(response):
    # pylint: enable=unused-argument
    """Check if string matches with user password when it comes on header"""
    if 'pswdtk' in request.headers:
        # argumentos = request.args.to_dict()
        try:
            user_query = json.loads(request.args.to_dict()['where'])
            user = app.data.pymongo().db.users.find_one(user_query)
            if user is None:
                app.logger.info('Can not find user')
                app.logger.info(user_query)
            if (BCRYPT.check_password_hash(user['auth']['password'],
                                           request.headers['pswdtk'])):
                return
        except Exception:
            print(traceback.format_exc())
        abort(401, description='Wrong password')
# pylint: enable=broad-except

# pylint: disable=unused-argument
def pre_get_user_exists(original_request, lookup):
    """ Prevent get on many users """
    has_where = original_request.args.to_dict().get('where', None)
    if not has_where:
        abort(401, description='Where have to be present')
    else:
        has_where = json.loads(has_where)
        if not isinstance(has_where['email'], str):
            abort(401, description='String must be passed')
        elif not bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                               has_where['email'])):
            abort(401, description='String must be a email form')

def before_returning_users_exists(response):
    """ Deleting etag on response """
    for item_response in response['_items']:
        del item_response['_etag']

# --- Main program ---
# pylint: disable=no-member
app.on_insert_users += before_insert
app.on_fetched_resource_auth += authenticate
app.on_update_user_admin += before_update
app.on_pre_GET_users_exists += pre_get_user_exists
app.on_fetched_resource_users_exists += before_returning_users_exists
# pylint: enable=no-member

if __name__ == '__main__':
    # the default log level is set to WARNING, so
    # we have to explictly set the logging level
    # to INFO to get our custom message logged.
    with app.test_request_context():
        insert_basic_data()
    ARGS = p.parse_args()
    if not ARGS.basic_data:
        app.run(debug=True, host='0.0.0.0', port=8000)
