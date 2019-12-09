import json
from test_api import basicEveTest, loggedBasicTest

class TestModule(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'modules'

    def test_get_public(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, 200, response.data)
    
    def test_post_private(self):
        data = {
            "name": "testando",
            "slug": "testando",
            "icon": "teste",
            "link": "/teste",
            "description": "testando a parada",
            "locked": True
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 401, response.data)

class TestModuleAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'modules'

    def test_post(self):
        data = {
            "name": "testando",
            "slug": "testando",
            "icon": "teste",
            "link": "/teste",
            "description": "testando a parada",
            "locked": True
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201,response.data)
        self.add_to_exclude_db(self.loads_response(response), collection='module')