""" Module plan """

PLAN_SCHEMA = {
    'email': {
        'type': 'string',
        'required': True,
        'regex':r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    },
    'admin_permission': {'type': 'boolean', 'default': False},
    'website': {'type': 'string'},
    'permission': {'type': 'string'},
    'settings': {
        'type': 'dict',
        'schema': {
            'transitions': {'type': 'boolean', 'default': True}
        }
    }
}

PLAN_PERMISSION_AGGREGATION = [
    {
        '$lookup': {
            'from': 'permission',
            'localField': 'permission',
            'foreignField': 'slug',
            'as': 'permission'
        }
    },
    {
        '$project': {
            'email': 1,
            'website': 1,
            'admin_permission': 1,
            '_updated': 1,
            '_created': 1,
            '_deleted': 1,
            'permission': {
                '$arrayElemAt': [
                    '$permission', 0
                ]
            }
        }
    },
    {
        '$lookup': {
            'from': 'group',
            'let': {
                'group_id': '$permission.group'
            },
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$and': [
                                {
                                    '$eq': [
                                        '$_id', '$$group_id'
                                    ]
                                }
                            ]
                        }
                    }
                }
            ],
            'as': 'permission.group'
        }
    },
    {
        '$project': {
            'email': 1,
            'website': 1,
            'admin_permission': 1,
            '_updated': 1,
            '_created': 1,
            'permission': {
                'name': 1,
                'slug': 1,
                '_updated': 1,
                '_created': 1,
                'modules': 1,
                'group': {
                    '$arrayElemAt': [
                        '$permission.group', 0
                    ]
                }
            }
        }
    },
    {
        '$project': {
            'email': 1,
            'website': 1,
            'admin_permission': 1,
            '_updated': 1,
            '_created': 1,
            'permission': {
                'name': 1,
                'slug': 1,
                '_updated': 1,
                '_created': 1,
                'group_name': '$permission.group.name',
                'group_slug': '$permission.group.slug',
                'collections': '$permission.group.collections',
                'modules': {
                    'admin': {
                        '$concatArrays': [
                            '$permission.group.modules.basic', '$permission.modules.admin'
                        ]
                    },
                    'desktop': {
                        '$concatArrays': [
                            '$permission.group.modules.basic',
                            '$permission.group.modules.desktop',
                            '$permission.modules.desktop'
                        ]
                    },
                    'app': {
                        '$concatArrays': [
                            '$permission.group.modules.basic',
                            '$permission.group.modules.app',
                            '$permission.modules.app'
                        ]
                    }
                }
            }
        }
    }
]
