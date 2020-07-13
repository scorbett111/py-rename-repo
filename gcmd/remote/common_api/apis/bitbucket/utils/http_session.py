import urllib
import json
import requests
from .request_decorator import http_handler


class HttpSession:

    def __init__(self, auth=None, base_url=None):
        self.url_store = {
            'default': base_url
        }

        if auth.type == 'token':
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(
                    token=auth.token
                )
            })
        
        else:
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
            self.session.auth = (auth.user, auth.password)

    def update_url_store(self, key=None, base=None, endpoint=None):
        self.url_store[key] = '{base_url}/{endpoint}'.format(
            base_url=self.url_store.get(base, 'default'),
            endpoint=endpoint
        )

    def delete_url(self, key=None):
        if self.url_store.get('key'):
            del self.url_store[key]

    @http_handler
    def get(self, url=None, key=None, endpoint=None):
        return self.session.get(endpoint)

    @http_handler
    def post(self, url=None, key=None, endpoint=None, data=None):
        return self.session.post(
            endpoint,
            data=json.dumps(data)
        )

    @http_handler
    def put(self, url=None, key=None, endpoint=None, data=None):
        return self.session.put(
            endpoint,
            data=json.dumps(data)
        )

    @http_handler
    def delete(self, url=None, key=None, endpoint=None):
        return self.session.delete()