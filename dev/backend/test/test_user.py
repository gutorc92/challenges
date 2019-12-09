import json
from test_api import basicEveTest
from datetime import datetime
from copy import copy


class TestUserAPI(basicEveTest):

    """Basic User endpoint test

    Should test the basic endpoint of the user
    """

    def test_filer_email(self):
        response = self.get('/user/exists?where={"email":{"$exists":0}}')
        self.assertEqual(response.status_code, 401)

    def test_update_user(self):
        valid_user = {
            "email": "teste@domain.com",
            "activated": True,
            "info": {
                "avatar": "man.jpg",
                "name": "teste",
                "surname": "teste"
            },
            "auth": {
                "password": "123123"
            }
        }
        response = self.post('/user/admin', json.dumps(valid_user))
        self.assertEqual(response.status_code, 201, response.data)
        user_created = self.loads_response(response)
        self.add_to_exclude_db(user_created, collection='users')
        local_headers = copy(self.headers)
        local_headers['If-Match'] = user_created['_etag']
        valid_user['info']['name'] = 'teste de atualização'
        response = self.test_client.patch(
            '/user/admin/{}'.format(user_created['_id']), headers=local_headers, data=json.dumps(valid_user))
        self.assertEqual(response.status_code, 200)

    def test_add_auth(self):
        valid_user = {
            'email': 'testehash@domain.com',
            'activated': True,
            'info': {
                'avatar': "man.jpg",
                'name': "teste",
                'surname': "teste"
            },
            'auth': {
                'password': '123123'
            }
        }
        valid_plan = {
            'email': 'testehash@domain.com',
            'website': 'localhost',
            'permission': 'normal-user',
            'admin_permission': False
        }
        with self.app.app_context():
            self.app.data.pymongo().db['plan'].insert_one(valid_plan)
        response = self.post('/user/admin', json.dumps(valid_user))
        self.assertEqual(response.status_code, 201, response.data)
        user_created = self.loads_response(response)
        self.add_to_exclude_db(user_created, collection='users')
        local_headers = copy(self.headers)
        local_headers['googleHash'] = 'DinoHash'
        response = self.test_client.post('/user/auth',
                      headers=local_headers,
                      data=json.dumps({
                        'email': valid_user['email'],
                        'website': 'localhost',
                        'location': {}
                      }))
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user_find = self.app.data.pymongo().db.users.find_one({'email': valid_user['email']})
        self.assertIn('auth', user_find)
        self.assertIn('googleHash', user_find['auth'])
        self.assertEqual(user_find['auth']['googleHash'], 'DinoHash', user_find)

    def test_login_user(self):
        valid_user = {
            'email': 'testepassword@domain.com',
            'activated': True,
            'info': {
                'avatar': "man.jpg",
                'name': "teste",
                'surname': "teste"
            },
            'auth': {
                'password': '123123'
            }
        }
        valid_plan = {
            'email': 'testepassword@domain.com',
            'website': 'localhost',
            'permission': 'normal-user',
            'admin_permission': False
        }
        with self.app.app_context():
            self.app.data.pymongo().db['plan'].insert_one(valid_plan)
        response = self.post('/user/admin', json.dumps(valid_user))
        self.assertEqual(response.status_code, 201, response.data)
        user_created = self.loads_response(response)
        self.add_to_exclude_db(user_created, collection='users')
        local_headers = copy(self.headers)
        local_headers['pswdtk'] = valid_user['auth']['password']
        response = self.test_client.post(
            '/user/auth', headers=local_headers, data=json.dumps({
                'email': valid_user['email'],
                'website': 'localhost',
                'location': {}
            }))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response['logged'], True, response)
        self.assertIn('token', response)
        local_headers['pswdtk'] = '123123fsdfs'
        response = self.test_client.post(
            '/user/auth', headers=self.headers, data=json.dumps({'email': valid_user['email']}))
        self.assertEqual(response.status_code, 401)
        response = json.loads(response.data.decode("utf-8"))
        # self.assertFalse(response['result'])
        self.assertEqual(response['_error']['message'], 'Invalid auth')
    
    def test_inactivated_user(self):
        inactivated_user = {
                'email': 'teste2@domain.com',
                'activated': False,
                'info': {
                    'avatar': "man.jpg",
                    'name': "teste",
                    'surname': "teste"
                },
                'auth': {
                    'password': '123123'
                }
        }
        valid_plan = {
            'email': 'teste2@domain.com',
            'website': 'localhost',
            'permission': 'normal-user',
            'admin_permission': False
        }
        with self.app.app_context():
            self.app.data.pymongo().db['plan'].insert_one(valid_plan)
        response = self.post('/user/admin', json.dumps(inactivated_user))
        self.assertEqual(response.status_code, 201, response.data)
        self.add_to_exclude_db(self.loads_response(response), collection='users')
        local_headers = copy(self.headers)
        with self.app.app_context():
            self.app.data.pymongo().db.users.update_one({'email': inactivated_user['email']}, {
                '$set': 
                    {'_created': datetime.strptime('Dec 1 2018  1:33PM', '%b %d %Y %I:%M%p')}
            })
        local_headers['pswdtk'] = '123123'
        response = self.test_client.post(
            '/user/auth', headers=local_headers, data=json.dumps({
              'email': 'teste2@domain.com',
              'website': 'localhost',
              'location': {}
        }))
        self.assertEqual(response.status_code, 401)
        response = json.loads(response.data.decode("utf-8"))
        # self.assertFalse(response['result'])
        self.assertEqual(response['_error']['message'], 'User not activated')