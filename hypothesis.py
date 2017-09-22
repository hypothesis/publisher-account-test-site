import datetime
import json
from urlparse import urlparse

import jwt
import requests


def _extract_domain(url):
    host_and_port = urlparse(url).netloc
    return host_and_port.split(':')[0]


class HypothesisClient(object):

    def __init__(self, client_id, client_secret, jwt_client_id,
                 jwt_client_secret, authority, service):
        self.authority = authority
        self.client_id = client_id
        self.client_secret = client_secret
        self.jwt_client_id = jwt_client_id
        self.jwt_client_secret = jwt_client_secret
        self.service = service

    def create_account(self, username, email, display_name=None):
        """
        Create an account on the Hypothesis service.

        This creates an account on the Hypothesis service, in the publisher's
        namespace, with the given `username` and `email`.
        """
        data = {'authority': self.authority,
                'username': username,
                'email': email,
                'display_name': display_name,
                }
        return self._make_request('POST', 'users', data)

    def update_account(self, username, email=None, display_name=None):
        data = {}
        if email is not None:
            data['email'] = email
        if display_name is not None:
            data['display_name'] = display_name
        return self._make_request('PATCH', 'users/{}'.format(username), data)

    def _make_request(self, method, path, data):
        auth = (self.client_id, self.client_secret)
        rsp = requests.request(
            method,
            '{}/api/{}'.format(self.service, path),
            data=json.dumps(data),
            auth=auth,
            # Don't verify SSL certificates if posting to localhost.
            verify=urlparse(self.service).hostname != 'localhost')
        rsp.raise_for_status()
        return rsp.json()

    def grant_token(self, username):
        """
        Create a grant token for the given `user`.

        This creates a grant token which can be passed to the Hypothesis client
        in order to enable it to view and create annotations as the given
        `username` within the publisher's accounts.
        """
        now = datetime.datetime.utcnow()
        claims = {
            'aud': _extract_domain(self.service),
            'iss': self.jwt_client_id,
            'sub': 'acct:{}@{}'.format(username, self.authority),
            'nbf': now,
            'exp': now + datetime.timedelta(minutes=5),
        }
        return jwt.encode(claims, self.jwt_client_secret, algorithm='HS256')
