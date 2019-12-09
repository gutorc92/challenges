import json
from test_api import basicEveTest, loggedBasicTest

class TestBattle(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'battle'
    
    def test_post_private(self):
        data = {
            'heroes': [],
            'dangerLevel': 'S',
            'monsterName': 'Black Dragon'
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 401, response.data)

class TestBattleAPI(loggedBasicTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'battle'

    def test_post(self):
        data = {
            'name': 'Teste',
            'class': 'S'
        }
        response = self.post('heroe', data=json.dumps(data))
        self.assertEqual(response.status_code, 201,response.data)
        response = self.loads_response(response)
        data = {
            'heroes': [response['_id']],
            'dangerLevel': 'S',
            'monsterName': 'Black Dragon'
        }
        response = self.post(self.url,
                      data=json.dumps(data))
        self.assertEqual(response.status_code, 201, response.data)
        self.add_to_exclude_db(self.loads_response(response))

    