import json
from test_api import basicEveTest, loggedBasicTest

class TestPlanCredentials(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'plan'

    def test_get_public(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, 401, response.data)

class TestPlanAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'plan'

    def test_post(self):
        data = {
            'email': 'teste@teste.com',
            'website': 'teste',
            'permission': 'teste',
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201,response.data)
        self.add_to_exclude_db(self.loads_response(response))