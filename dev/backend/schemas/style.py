""" Module style """

STYLE_SCHEMA = {
    'name': {'type': 'string', 'required': True},
    'slug': {'type': 'string', 'required': True, 'unique': True},
    'descriptions': {
        'type': 'dict',
        'schema': {
            'default': {'type': 'string', 'default': ''}
        }
    },
    'images': {
        'type': 'dict',
        'schema': {
            'login_banner': {'type': 'string', 'default': ''},
            'login_logo': {'type': 'string', 'default': ''},
            'banner_email': {'type': 'string', 'default': ''},
            'banner': {'type': 'string', 'default': 'statics/oab-banner.png'},
            'logo': {'type': 'string', 'default': ''}
        }
    },
    'color': {
        'type': 'dict',
        'schema': {
            'primary': {'type': 'string', 'default': '#a6ce38'},
            'secondary': {'type': 'string', 'default': '#016db9'},
            'tertiary': {'type': 'string', 'default': '#00b1e6'},
            'neutral': {'type': 'string', 'default': '#f2f2f2'},
            'positive': {'type': 'string', 'default': '#01b32d'},
            'negative': {'type': 'string', 'default': '#e74c3c'},
            'info': {'type': 'string', 'default': '#005ac3'},
            'warning': {'type': 'string', 'default': '#f1c40f'},
            'banner_skin': {'type': 'string', 'default': '#2ea524b3'},
        }
    },
    'external_media': {
        'type': 'dict',
        'schema': {
            'youtube': {'type': 'string', 'default': ''},
            'instagram': {'type': 'string', 'default': ''},
            'facebook': {'type': 'string', 'default': ''},
        }
    }
}
