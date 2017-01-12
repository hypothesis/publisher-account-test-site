import datetime
import json
import jwt
import requests


class HypothesisClient(object):

    def __init__(self, client_id, client_secret, authority, service):
        self.authority = authority
        self.client_id = client_id
        self.client_secret = client_secret
        self.service = service

    def create_account(self, username, email):
        """
        Create an account on the Hypothesis service.

        This creates an account on the Hypothesis service, in the publisher's
        namespace, with the given `username` and `email`.
        """
        auth = (self.client_id, self.client_secret)

        data = {'authority': self.authority,
                'username': username,
                'email': email,
                }

        rsp = requests.post('{}/api/users'.format(self.service),
                            data=json.dumps(data), auth=auth)
        rsp.raise_for_status()

    def grant_token(self, username):
        """
        Create a grant token for the given `user`.

        This creates a grant token which can be passed to the Hypothesis client
        in order to enable it to view and create annotations as the given
        `username` within the publisher's accounts.
        """
        now = datetime.datetime.utcnow()
        claims = {
            'aud': self.service,
            'iss': self.client_id,
            'sub': 'acct:{}@{}'.format(username, self.authority),
            'nbf': now,
            'exp': now + datetime.timedelta(minutes=30),
        }
        return jwt.encode(claims, self.client_secret, algorithm='HS256')
