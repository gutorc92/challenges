""" Module module """

MODULE_SCHEMA = {
    'name': {'type': 'string', 'required': True},
    'slug': {'type': 'string', 'required': True},
    'icon': {'type': 'string', 'default': ''},
    'link': {'type': 'string', 'default': ''},
    'description': {'type': 'string', 'default': ''},
    'locked': {'type': 'boolean', 'default': False} # locked when user is a begginer
}
