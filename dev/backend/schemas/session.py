""" Module session """

SESSION_SCHEMA = {
    'user_id': {'type': 'objectid', 'required': True},
    'website': {'type': 'string'},
    'token': {
        'type': 'dict',
        'schema': {
            'token_str': {'type': 'string', 'required': True},
            'created': {'type': 'datetime', 'required': True},
            'expires_in': {'type': 'datetime', 'required': True},
            'expired': {'type': 'boolean', 'default': False},
            'refresh_token': {'type': 'string', 'required': True}
        }
    },
    'location': {
        'type': 'dict',
        'schema': {
            'ip': {'type': 'string'},
            'loc': {'type': 'point'},
            'country': {'type': 'string'},
            'region': {'type': 'string'},
            'city': {'type': 'string'}
        }
    },
    'device': {
        'type': 'dict',
        'allow_unknown': True
    }
}
