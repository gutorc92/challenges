import json
from test_api import basicEveTest


class TestStyleAPI(basicEveTest):

    """Basic User endpoint test
    Should test the basic endpoint of the user
    """
    url = 'style'

    def test_post(self):
        style = {
            'name': 'teste',
            'slug': 'teste-teste',
            'descriptions': {
                'default': 'Testando'
            },
            'images': {
                'login_banner': 'logo-teste.jpg',
                'login_logo': 'logo-login-test.jpg',
                'banner_email': 'banner-email-test.jpg',
                'banner': 'banner-test.jpg',
                'logo': 'logo-test.jps'
            },
            'color': {
                'primary': '#a6ce38',
                'secondary': '#016db9',
                'tertiary': '#00b1e6',
                'neutral': '#f2f2f2',
                'positive': '#01b32d',
                'negative': '#e74c3c',
                'info': '#005ac3',
                'warning': '#f1c40f',
                'banner_skin': '#2ea524b3',
            },
            'external_media': {
                'youtube': 'https://youtube.com',
                'instagram': 'https://instagram.com',
                'facebook': 'https://facebook.com',
            }
        }
        response = self.post(self.url,
                      data=json.dumps(style))
        self.assertEqual(response.status_code, 201,response.data)
        self.add_to_exclude_db(self.loads_response(response))