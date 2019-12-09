""" Authenticate user """
from os import environ
import traceback
#pylint: disable=ungrouped-imports
try:
    from secrets import token_hex
except ImportError:
    from os import urandom
    def token_hex(nbytes=None):
        """ Token hex """
        return urandom(nbytes).hex()
#pylint: enable=ungrouped-imports
import json
import re
from datetime import datetime, timedelta
from copy import copy
from bson.objectid import ObjectId
from bson import json_util
from dotenv import load_dotenv, find_dotenv
from jose import jwt
from flask import current_app, request
from eve.methods.post import post_internal
from schemas import PLAN_PERMISSION_AGGREGATION

try:
    load_dotenv(find_dotenv())
except IOError as exception:
    pass

DAYS_TO_ACTIVATE = int(environ.get("DAYS_TO_ACTIVATE", 10))
VALID_SOCIAL = {'googlehash': 'googleHash', 'facebookhash': 'facebookHash'}

class GrAuth():
    """ Manage all possible auths"""

    def __init__(self, app=None):
        """setup"""
        self.app = app if app else current_app
        with self.app.app_context():
            self.users = self.app.data.pymongo().db.users
            self.integration = self.app.data.pymongo().db.integration

    # pylint: disable=no-else-return
    def authenticate(self):
        """general auth"""
        argumentos = json.loads(request.data.decode('utf-8'))
        headers = dict(request.headers)
        regex = re.compile(r'.*hash$')
        social_media = set(filter(regex.search, headers.keys()))
        social_media = set(map(str.lower, social_media))
        if request.headers.get('pswdtk'):
            return self.password_auth()
        elif social_media:
            return self.social_auth(social_media)
        elif 'integration' in argumentos:
            return self.integration_auth()
        raise Exception('Invalid auth')
    # pylint: enable=no-else-return

    def _get_user_(self, email, integration=False):
        """find a valid user"""
        user = self.users.find_one({'email': email})
        if not user:
            raise Exception('User not found')
        if integration:
            return user
        try:
            today = datetime.utcnow().replace(tzinfo=user['_created'].tzinfo)
            delta = (today.date() - user['_created'].date()).days
        except Exception:
            delta = 10
        if user['activated'] is False and delta > DAYS_TO_ACTIVATE:
            self.app.logger.info('User: %s not activated', email)
            raise Exception('User not activated')
        return user

    def logout(self):
        """logout user"""
        try:
            argumentos = json.loads(request.data.decode('utf-8'))
            email = str(argumentos['email'])
            website = str(argumentos['website'])
            print('argumentos', email)
            user = self._get_user_(email)
            today = datetime.now()
            result = self.app.data.pymongo().db.session.update_one(
                {
                    'user_id': ObjectId(str(user['_id'])),
                    'website': website,
                },
                {
                    '$set':
                        {
                            'token.expired': True,
                            'update_at': today
                        }
                }
            )
            if result.modified_count == 1:
                return True
            return False
        except Exception:
            traceback.print_exc()
            return False
    # pylint: enable=broad-except

    def password_auth(self):
        """auth with password"""
        password = request.headers.get('pswdtk')
        argumentos = json.loads(request.data.decode('utf-8'))
        email = str(argumentos['email'])
        user = self._get_user_(email)
        result = False
        token = message = plan = ''
        result = self.app.__bcrypt__.check_password_hash(
            user['auth']['password'], password
        )
        if result:
            message = 'OK'
            result, token, message, plan = self.register_session(argumentos, user)
        else:
            message = 'Wrong Password'
        return {
            'result': result,
            'email': email,
            'message': message,
            'token': token,
            "logged": result,
            "plan": plan
        }

    def find_plan(self, email, website):
        """ Find plan of user for a given website """
        plan = None
        match = {
            '$match': {
                'email': email,
                'website': website
            }
        }
        pipelene = copy(PLAN_PERMISSION_AGGREGATION)
        pipelene.insert(0, match)
        try:
            plan = self.app.data.pymongo().db.plan.aggregate(pipelene).next()
        except StopIteration:
            traceback.print_exc()
        return plan

    # pylint: disable=broad-except
    def register_session(self, argumentos, user):
        """ Register session """
        website = str(argumentos['website'])
        location = argumentos['location']
        token_generated = token_hex(256)
        today = datetime.now()
        message = 'Wrong Situation'
        result = False
        plan = self.find_plan(user['email'], website)
        if not plan:
            result = False
            message = 'Plan not find'
            return result, '', message, plan
        try:
            session = {
                'website': website,
                'user_id': user['_id'],
                'location': location,
                'token': {
                    'token_str': token_generated,
                    'created': today,
                    'expires_in': today + timedelta(minutes=5),
                    'expired': False,
                    'refresh_token': '12345'
                }
            }
            _, _, _, return_code, _ = post_internal('session', session)
            token = str(user['_id']) + '-' + token_generated
            if return_code == 201:
                result = True
                message = 'OK'
            if self.app.gr_cache:
                self.app.gr_cache.set(str(user['_id']),
                                      json.dumps(session, default=json_util.default),
                                      ex=60 * 5)
                result = True
                message = 'OK'
        except Exception:
            traceback.print_exc()
        token = token if result is True else ''
        return result, token, message, plan
      # pylint: enable=broad-except

    def social_auth(self, social_media):
        """auth with social media"""
        if social_media.intersection(VALID_SOCIAL.keys()):
            social_media = VALID_SOCIAL[social_media.pop()]
            social_hash = request.headers.get(social_media)
        else:
            raise Exception('Invalid Social Media')

        argumentos = json.loads(request.data.decode('utf-8'))
        email = str(argumentos['email'])
        user = self._get_user_(email)

        if user['auth'].get(social_media):
            logged = user['auth'].get(social_media) == social_hash
            result = logged
            message = 'OK' if result else 'Invalid Credentials'
        else:
            results = self.users.update_one(
                {'email': email},
                {"$set": {"auth." + social_media: social_hash}})
            result = results.acknowledged
            logged = result
            message = 'Credentials Updated' if result else str(results.raw_result)
        return {
            'result': result,
            'email': email,
            'message': message,
            "logged": logged,
        }

    # pylint: disable=broad-except
    def integration_auth(self):
        """auth with JWT integration"""
        argumentos = json.loads(request.data.decode('utf-8'))
        integration = self.integration.find_one(
            {'slug': argumentos['integration']}
        )
        if not integration:
            raise Exception('Invalid Integration')
        token = request.headers.get('token')
        try:
            token_decode = jwt.decode(token, integration.get('token'), algorithms=['HS256'])
        except Exception:
            token_decode = {}
        email = token_decode.get('email')
        if not email:
            raise Exception('Missing user in payload')
        user = self._get_user_(email, integration=True)
        token_integration = token_decode.get('token', '--')
        result = user.get('auth').get('token') == token_integration
        message = 'OK' if result else 'Invalid Credentials'
        return {
            'result': result,
            'email': email,
            'message': message,
            "logged": result
        }
    # pylint: enable=broad-except
