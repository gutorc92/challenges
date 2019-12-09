import json
from test_api import basicEveTest, loggedBasicTest

class TestGroupCredentials(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'group'

    def test_get_public(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, 401, response.data)

class TestPermissionCredentials(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'permission'

    def test_get_public(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, 401, response.data)

class TestGroupAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'group'

    def test_post(self):
        data = {
            'name': 'Administrador',
            'slug': 'admin-teste',
            'collections': [],
            'modules': {
                'basic': ['testando'],
                'app': ['teste'],
                'desktop': ['teste-teset']
            }
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201,response.data)
        self.add_to_exclude_db(self.loads_response(response))

class TestPermissionAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'permission'

    def test_post(self):
        data = {
            'name': 'Usuário básico',
            'slug': 'basic',
            'collections': [],
            'modules': {
                'basic': ['testando'],
                'app': ['teste'],
                'desktop': ['teste-teset'],
                'admin': []
            }
        }
        response = self.post('group',
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201,response.data)
        group_created = self.loads_response(response)
        self.add_to_exclude_db(group_created, collection='group')
        data_permissions = {
            'name': 'teste basic',
            'slug': 'teste-basic',
            'group': str(group_created['_id']),
            'modules': {
                'app': [],
                'desktop': ['teste-menu'],
                'admin': []
            }
        }
        response = self.post(self.url,
                      data=json.dumps(data_permissions))
        self.assertEqual(response.status_code, 201,response.data)
        self.add_to_exclude_db(self.loads_response(response))
