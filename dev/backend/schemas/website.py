""" Module website """

MODULE_PLACE_SCHEMA = {
    'place': {'type': 'string', 'required': True},
    'items': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'order': {'type': 'integer', 'required': True, 'nullable': False},
                'item': {'type': 'string', 'required': True, 'nullable': False},
            }
        }
    }
}

# pylint:disable=duplicate-code
WEB_SITE_SCHEMA = {
    'url': {'type': 'string', 'required': True, 'nullable': False},
    'slug': {'type': 'string', 'required': True, 'unique': True},
    'style': {'type': 'string', 'required': True},
    'components': {
        'type': 'dict',
        'schema': {
            'main': {'type': 'string'},
            'welcome': {'type': 'string'}
        }
    },
    'menu': {
        'type': 'dict',
        'schema': {
            'type': {
                'type': 'string',
                'allowed': ['left-drawer', 'toolbar'],
                'default': 'left-drawer'
            }
        }
    },
    'modules': {
        'type': 'dict',
        'schema': {
            'public': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': MODULE_PLACE_SCHEMA
                }
            },
            'private': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': MODULE_PLACE_SCHEMA
                }
            }
        }
    }
}
