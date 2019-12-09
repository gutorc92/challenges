""" Module heroes """

HEROES_SCHEMA = {
    'name': {'type': 'string'},
    'class': {'type': 'string'}
}

BATTLE_HISTORY = {
    'heroes': {
        'type': 'list',
        'schema': {
            'type': 'objectid'
        }
    },
    'dangerLevel': {'type': 'string'},
    'monsterName': {'type': 'string'}
}