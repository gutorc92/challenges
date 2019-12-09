"""
    Settings to be overwriten and used by API
"""
from os import environ
from schemas import STYLE_SCHEMA, WEB_SITE_SCHEMA, MODULE_SCHEMA
from schemas import GROUP_SCHEMA, PERMISSION_SCHEMA, USERS_SCHEMA
from schemas import PLAN_SCHEMA, SESSION_SCHEMA
from schemas import HEROES_SCHEMA, BATTLE_HISTORY
from utils import GrTokenAuth

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except IOError:
    pass

MONGO_HOST = environ.get("MONGO_HOST", 'localhost')
# MONGO_PORT = int(environ.get("MONGO_PORT"))
MONGO_DBNAME = environ.get("MONGO_DBNAME", 'postpress')

# Skip these if your db has no auth. But it really should.
# MONGO_USERNAME = environ.get("MONGO_USER")
# MONGO_PASSWORD = environ.get("MONGO_PASS")
# MONGO_AUTH_SOURCE = environ.get("MONGO_USER")

MONGO_QUERY_BLACKLIST = ['$where']
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

XML = False
JSON = True
X_DOMAINS = '*'
X_HEADERS = ['Authorization', 'Content-type', 'Cache-Control',
             'If-Match', 'pswdtk', 'UserEmail']

CACHE_EXPIRES = 10
# PAGINATION_LIMIT = 1000
PAGINATION_DEFAULT = 30
AUTO_CREATE_LISTS = True
SOFT_DELETE = True


# --- Schemas ---
# pylint: disable=invalid-name



users = {
    'schema': USERS_SCHEMA,
    'url': 'user/admin',
    'resource_methods': ['POST'],
    'resouce'
    'datasource': {
        'filter': {
            '_deleted': {"$ne": True},
            # 'correct_answer': {'$exists': True},  # apenas questões com respostas
            # 'is_nullified': False,  # apenas questões que não foram anuladas
            # 'showing': True
        },
        'source': 'users',
        'projection': {  # campos para serem omitidos
            'auth': 0,
            'info_b2b': 0
        }
    },
}



users_exists = {
    'schema': USERS_SCHEMA,
    'url': 'user/exists',
    'allowed_filters': ['email'],
    'resource_methods': ["GET"],
    'hateoas': False,
    'datasource': {
        'filter': {
            '_deleted': False,
        },
        'source': environ.get("MONGO_HOST_USER", 'users'),
        'projection': {  # campos para serem omitidos
            'email': 1
        }
    },
}

users_login = {
    'schema': USERS_SCHEMA,
    'authentication': GrTokenAuth,
    'url': 'user/login',
    'allowed_filters': ['email'],
    'datasource': {
        'filter': {
            '_deleted': {"$ne": True},
            # 'correct_answer': {'$exists': True},  # apenas questões com respostas
            # 'is_nullified': False,  # apenas questões que não foram anuladas
            # 'showing': True
        },
        'source': environ.get("MONGO_HOST_USER", 'users'),
        'projection': {  # campos para serem omitidos
            'auth': 0
        }
    },
}

users_list = {
    'schema': USERS_SCHEMA,
    'authentication': GrTokenAuth,
    'url': 'user/list',
    'datasource': {
        'filter': {
            '_deleted': {"$ne": True},
            # 'correct_answer': {'$exists': True},  # apenas questões com respostas
            # 'is_nullified': False,  # apenas questões que não foram anuladas
            # 'showing': True
        },
        'source': environ.get("MONGO_HOST_USER", 'users'),
        'projection': {  # campos para serem omitidos
            'auth': 0
        }
    },
}

DOMAIN = {
    'users': users,
    'users_exists': users_exists,
    'user_login': users_login,
    'users_list': users_list,
    'module': {
        'schema': MODULE_SCHEMA,
        'authentication': GrTokenAuth,
        'public_methods': ['GET'],
        'url': 'modules',
    },
    'heroe': {
        'schema': HEROES_SCHEMA,
        'authentication': GrTokenAuth,
        'resource_methods': ['POST', 'GET'],
    },
    'battle': {
        'schema': BATTLE_HISTORY,
        'authentication': GrTokenAuth
    },
    'website_public': {
        'schema': WEB_SITE_SCHEMA,
        'url': 'website/public',
        'public_methods': ['GET'],
        'datasource': {
            'source': 'website',
            'projection': {  # campos para serem omitidos
                "modules.public": 1,
                "components.main": 1,
                "slug": 1,
                "menu": 1,
                "style": 1
            }
        }
    },
    'website_private': {
        'schema': WEB_SITE_SCHEMA,
        'url': 'website/private',
        'authentication': GrTokenAuth,
        'datasource': {
            'source': 'website'
        }
    },
    'style': {
        'schema': STYLE_SCHEMA
    },
    'group': {
        'schema': GROUP_SCHEMA,
        'authentication': GrTokenAuth,
    },
    'permission': {
        'schema': PERMISSION_SCHEMA,
        'authentication': GrTokenAuth,
    },
    'plan': {
        'schema': PLAN_SCHEMA,
        'authentication': GrTokenAuth,
    },
    'session': {
        'schema': SESSION_SCHEMA
    }
}
