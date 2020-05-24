""" Basic data """
DATA = [
    # {
    #     'resource': 'user_admin',
    #     'field': 'email',
    #     'data': [
    #         {
    #             "email": "teste@domain.com",
    #             "activated": True,
    #             "info": {
    #                 "avatar": "man.jpg",
    #                 "name": "teste",
    #                 "surname": "teste"
    #             },
    #             "auth": {
    #                 "password": "123123"
    #             }
    #         }
    #     ]
    # },
    {
        'resource': 'style',
        'field': 'slug',
        'data': [
            {
                'name': 'Teste',
                'slug': 'teste',
                'descriptions': {
                    'default': 'Site de Herois'
                },
                'images': {
                    'login_banner': '',
                    'login_logo': '',
                    'banner_email': '',
                    'banner': '',
                    'logo': ''
                },
                'color': {
                    'primary': '',
                    'secondary': '',
                    'tertiary': '',
                    'neutral': '',
                    'positive': '',
                    'negative': '',
                    'info': '',
                    'warning': '',
                    'banner_skin': '',
                },
                'external_media': {
                    'youtube': '',
                    'instagram': '',
                    'facebook': '',
                }
            }
        ]
    },
    {
        'resource': 'group',
        'field': 'slug',
        'data': [
            {
                'name': 'Administrador',
                'slug': 'admin',
                'collections': [],
                'modules': {
                    'basic': ['users', 'modules', 'posts', 'style'],
                    'app': [],
                    'desktop': []
                }
            },
            {
                'name': 'Usuario',
                'slug': 'normal-user',
                'collections': [],
                'modules': {
                    'basic': ['login', 'logout', 'blog'],
                    'app': [],
                    'desktop': []
                }
            }
        ]
    },
    {
        'resource': 'permission',
        'field': 'slug',
        'relation': 'group',
        'data': [
            {
                'name': 'Administrador',
                'slug': 'admin',
                'group': {
                    'value': 'admin',
                    'reference': 'group',
                    'field_search': 'slug',
                    'field_value': '_id'
                },
                'modules': {
                    'admin': [''],
                    'app': [],
                    'desktop': ['']
                }
            },
            {
                'name': 'Usuário Padrão',
                'slug': 'normal-user',
                'group': {
                    'value': 'normal-user',
                    'reference': 'group',
                    'field_search': 'slug',
                    'field_value': '_id'
                },
                'modules': {
                    'admin': [''],
                    'app': [],
                    'desktop': ['battle', 'heroe']
                }
            },
        ]
    },
    {
        'resource': 'plan',
        'field': 'email',
        'data': [
            {
                'email': 'teste@teste.com',
                'website': 'teste',
                'permission': 'teste'
            },
        ]
    },
    {
        'resource': 'module',
        'field': 'slug',
        'data': [
            {
                'name': 'Usuários',
                'slug': 'users',
                'icon': 'supervised_user_circle',
                'link': '/users',
                'description': 'Módulo de usuários',
                'locked': False
            },
            {
                'name': 'Módulos',
                'slug': 'modules',
                'icon': 'list',
                'link': '/admin/modules/list',
                'description': 'Módulo de módulos',
                'locked': False
            },
            {
                'name': 'Posts',
                'slug': 'posts',
                'icon': 'list',
                'link': '/admin/posts/list',
                'description': 'Módulo de Posts',
                'locked': False
            },
            {
                'name': 'Estilos',
                'slug': 'style',
                'icon': 'view_list',
                'link': '/admin/style/list',
                'description': 'Módulo de estilos',
                'locked': False
            },
            {
                'name': 'Blog',
                'slug': 'blog',
                'icon': 'view_list',
                'link': '/blog',
                'description': 'Módulo de blog',
                'locked': False
            },
            {
                'name': 'Login',
                'slug': 'login',
                'icon': 'perm_contact_calendar',
                'link': '/login',
                'description': 'Módulo de Login',
                'locked': False
            },
            {
                'name': 'Logout',
                'slug': 'logout',
                'icon': 'exit_to_app',
                'link': '',
                'description': 'Módulo de Logout',
                'locked': False
            },
            {
                'name': 'Herois',
                'slug': 'heroe',
                'icon': 'list',
                'link': '/user/heroe',
                'description': 'Módulo de Heróis',
                'locked': False
            },
            {
                'name': 'Batalhas',
                'slug': 'battle',
                'icon': 'list',
                'link': '/user/battle',
                'description': 'Módulo de Batalhas',
                'locked': False
            }
        ]
    },
    {
        'resource': 'website_private',
        'field': 'slug',
        'data': [
            {
                'url': 'localhost',
                'slug': 'localhost',
                'style': 'teste',
                'menu': {
                    'type': 'left-drawer'
                },
                'modules': {
                    'public': [
                        {
                            'place': 'menu',
                            'items': [
                                {
                                    'order': 1,
                                    'item': 'blog'
                                },
                                {
                                    'order': 2,
                                    'item': 'login'
                                }
                            ]
                        }
                    ],
                    'private':  [
                        {
                            'place': 'menu',
                            'items': [
                                {
                                    'order': 1,
                                    'item': 'style'
                                },
                                {
                                    'order': 2,
                                    'item': 'users'
                                },
                                {
                                    'order': 3,
                                    'item': 'modules'
                                },
                                {
                                    'order': 4,
                                    'item': 'posts'
                                },
                                {
                                    'order': 5,
                                    'item': 'logout'
                                }
                            ]
                        },
                        {
                            'place': 'logout',
                            'items': [
                                {
                                    'order': 1,
                                    'item': 'logout'
                                }
                            ]
                        },
                        {
                            'place': 'menu-user',
                            'items': [
                                {
                                    'order': 1,
                                    'item': 'heroe'
                                },
                                {
                                  'order': 2,
                                  'item': 'battle'
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
]
