""" Module user """

USERS_SCHEMA = {
    '_id': {'type': 'objectid', 'unique': True, },
    'email': {
        'type': 'string',
        'unique': True,
        'required': True,
        'regex':r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        },
    'activated': {'type': 'boolean', 'default': False},
    'auth': {
        'type': 'dict',
        'schema': {
            'password': {'type': 'string', 'required': False, 'nullable': True},
            'googleHash': {'type': 'string', 'required': False, 'nullable': True},
            'facebookHash': {'type': 'string', 'required': False, 'nullable': True}
        },
        'required': True
    },
    'info': {
        'type': 'dict',
        'schema': {
            'avatar': {'type': 'string', 'default': "statics/man.jpg"},
            'name': {'type': 'string'},
            'surname': {'type': 'string'}
        }
    },
    'comment': {'type': 'string', 'default': ''},
}
