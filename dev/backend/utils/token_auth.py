""" Module auth """
import traceback
import json
from flask import current_app as app
from eve.auth import TokenAuth
from bson.objectid import ObjectId
from bson import json_util
from .gr_cache import Cache

class GrTokenAuth(TokenAuth):
    """ Token auth """

    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        # use Eve's own db driver; no additional connections/resources are used
        try:
            print('token', token)
            id_user, hash_token = token.split('-')
            if isinstance(app.gr_cache, Cache):
                session = app.data.driver.db['session']
                return session.find_one({
                    'token.token_str': hash_token,
                    'token.expired': False,
                    'user_id': ObjectId(id_user)
                })
            session = json.loads(app.gr_cache.get(id_user), object_hook=json_util.object_hook)
            return bool(session['token']['token_str'] == hash_token)
        except Exception:
            traceback.print_exc()
            return False
