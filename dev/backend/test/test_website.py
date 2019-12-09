import json
from test_api import basicEveTest, loggedBasicTest

class TestWebSitePublicAPI(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'website/public'

    def test_get_public(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, 200, response.data)
    
    def test_get_private(self):
        response = self.get('website/private')
        self.assertEqual(response.status_code, 401, response.data)

class TestWebSiteAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'website/private'

    def test_post(self):
        website = {
            'url': 'test.com',
            'slug': 'testando',
            'style': 'test-style',
            'components': {
                'main': 'teste',
                'welcome': 'teste'
            },
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
                                'item': 'painel'
                            },
                            {
                                'order': 2,
                                'item': 'users'
                            }
                        ]
                    },
                    {
                        'place': 'list-users',
                        'items': [
                            {
                                'order': 1,
                                'item': 'edit-user'
                            },
                            {
                                'order': 2,
                                'item': 'delete-user'
                            }
                        ]
                    }
                ],
                'private': []
            }
        }
        response = self.post(self.url,
                      data=json.dumps(website))
        self.assertEqual(response.status_code, 201, response.data)
        self.add_to_exclude_db(self.loads_response(response), collection='website')

    