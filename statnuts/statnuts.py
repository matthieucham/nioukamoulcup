__author__ = 'Matt'

import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


class StatnutsClient():
    def __init__(self, cl_id, cl_secret, sn_base_url):
        self.client_id = cl_id
        self.client_secret = cl_secret
        self.sn_base_url = sn_base_url
        self.token_url = sn_base_url + '/o/token/'
        self.access_token = None
        self.oauth = OAuth2Session(client=BackendApplicationClient(client_id=self.client_id))

    def _get_access_token(self):
        token = self.oauth.fetch_token(token_url=self.token_url, client_id=self.client_id,
                                       client_secret=self.client_secret)
        return token

    def get_tournament_instance(self, saison_uuid):
        journees_url = '/rest/tournament_instances/%s/?expand=steps' % saison_uuid
        if self.access_token is None:
            self.access_token = self._get_access_token()
        data = self.oauth.get(self.sn_base_url+journees_url).json()
        return data

    def get_step(self, journee_uuid):
        rencontres_url = '/rest/steps/%s/?expand=meetings' % journee_uuid
        if self.access_token is None:
            self.access_token = self._get_access_token()
        data = self.oauth.get(self.sn_base_url+rencontres_url).json()
        return data