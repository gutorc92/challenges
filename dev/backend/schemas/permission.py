""" Module permission """

GROUP_SCHEMA = {
    'name': {'type': 'string', 'required': True},
    'slug': {'type': 'string', 'required': True, 'unique': True},
    'collections': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'modules': {
        'type': 'dict',
        'schema': {
            'basic': {'type': 'list', 'schema': {'type': 'string'}},
            'app': {'type': 'list', 'schema': {'type': 'string'}},
            'desktop': {'type': 'list', 'schema': {'type': 'string'}},
            'admin': {'type': 'list', 'schema': {'type': 'string'}}
        }
    }
}

PERMISSION_SCHEMA = {
    'name': {'type': 'string', 'required': True},
    'slug': {'type': 'string', 'required': True, 'unique': True},
    'group': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'group',
            'field': '_id',
            'embeddable': True
        },
    },
    'modules': {
        'type': 'dict',
        'schema': {
            'app': {'type': 'list', 'schema': {'type': 'string'}},
            'desktop': {'type': 'list', 'schema': {'type': 'string'}},
            'admin': {'type': 'list', 'schema': {'type': 'string'}}
        }
    }
}
