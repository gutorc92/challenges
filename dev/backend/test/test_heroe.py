import json
from test_api import basicEveTest, loggedBasicTest

class TestHeroe(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'heroe'

    
    def test_post_private(self):
        data = {
            'name': 'Teste',
            'class': 'S'
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 401, response.data)

class TestCommentAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'heroe'

    def test_post(self):
        data = {
            'name': 'Teste',
            'class': 'S'
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201, response.data)
        self.add_to_exclude_db(self.loads_response(response))

    