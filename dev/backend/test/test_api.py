import unittest
from eve import Eve
import os
from api import app
from copy import copy
import settings
from base64 import b64encode
from os import environ, path
from bson.objectid import ObjectId
from pymongo.errors import ServerSelectionTimeoutError
import json
from utils import insert_basic_data

try:
    load_dotenv(find_dotenv())
except Exception as e:
    pass


class basicEveTest(unittest.TestCase):
    """Basic Eve test class
    It should let a client available and a app.
    Make requests with:

    self.test_client.get('/endpoit')

    """

    url = ''
    

    def setUp(self):
        dir_path = path.dirname(path.realpath(__file__))
        # self.app = Eve(settings=dir_path+'/../settings.py')
        self.app = app
        self.test_client = self.app.test_client()
        hash = bytes(environ.get("MONGO_USER") + ':' +
                     environ.get("MONGO_PASS"), "utf-8")
        self.headers = {
            # 'Authorization': 'Basic %s' % b64encode(hash).decode("ascii"),
            'Content-Type': 'application/json'
        }
        self.excludes = {}
        self.excludes_db = {}

    
    def add_to_exclude_url(self, data, url=None):
        local_url = self.url if url is None else url
        print('local url', local_url)
        if local_url in self.excludes:
            self.excludes[local_url].append(data)
        else:
            self.excludes[local_url] = [data]
        from pprint import pprint
        pprint(self.excludes)
    
    def add_to_exclude_db(self, data, collection=None):
        local_collection = self.url if collection is None else collection
        if local_collection in self.excludes:
            self.excludes_db[local_collection].append(data)
        else:
            self.excludes_db[local_collection] = [data]
    
    def loads_response(self, response):
        return json.loads(response.data.decode('utf-8'))

    def tearDown(self):
        for url, data in self.excludes.items():
            print('excluindo', url)
            for item in data:
                local_headers = copy(self.headers)
                if '_id' in item and '_etag' in item:
                    local_headers['If-Match'] = item['_etag']
                    response = self.test_client.delete('/{}/{}'.format(url, item['_id']), headers=local_headers)
                    print('resposta exclusao', response)
        with self.app.app_context():
            for collection, data in self.excludes_db.items():
                for item in data:
                    if '_id' in item:
                        response = self.app.data.pymongo().db[collection].delete_one({'_id': ObjectId(item['_id'])})
                        # print('resposta exclusao', response.deleted_count)



    def get(self, url):
        try:
            response = self.test_client.get(url, headers=self.headers)
            return response
        except ServerSelectionTimeoutError as e:
            self.skipTest(str(response.response))

    def post(self, url, data):
        try:
            response = self.test_client.post(url, headers=self.headers, data=data)
            return response
        except ServerSelectionTimeoutError as e:
            self.skipTest(str(response.response))

class loggedBasicTest(basicEveTest):

    def setUp(self):
        super(loggedBasicTest, self).setUp()
        valid_user = {
            'email': 'testelogin@domain.com',
            'activated': True,
            'info': {
                'avatar': "man.jpg",
                'name': "teste",
                'surname': "teste"
            },
            'auth': {
                'password': '$2b$12$pXfMDTTp5Flr4PJchRrN2eQY7o/OuH3P9zpzk/bsAdtzuu0NAv9im'
            }
        }
        valid_plan = {
            'email': 'testelogin@domain.com',
            'website': 'localhost',
            'permission': 'normal-user',
            'admin_permission': False
        }
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
        with self.app.app_context():
          insert_basic_data()
        with self.app.app_context():
            self.app.data.pymongo().db['users'].insert_one(valid_user)
            self.app.data.pymongo().db['plan'].insert_one(valid_plan)
        local_headers = copy(self.headers)
        local_headers['pswdtk'] = '123123'
        response = self.test_client.post(
            '/user/auth', headers=local_headers, data=json.dumps({
                'email': valid_user['email'],
                'website': 'localhost',
                'location': {}
        }))
        response = json.loads(response.data.decode("utf-8"))
        self.headers['Authorization'] = "Bearer " + response['token']
        with self.app.app_context():
            user = self.app.data.pymongo().db['users'].find_one({'email': valid_user['email']})
            self.add_to_exclude_db(user, collection='users')

if __name__ == '__main__':
    unittest.main(verbosity=3)
