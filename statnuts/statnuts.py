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

    def _get_data(self, target_url):
        if self.access_token is None:
            self.access_token = self._get_access_token()
        data = self.oauth.get(self.sn_base_url+target_url).json()
        return data

    def get_tournament_instance(self, saison_uuid):
        journees_url = '/rest/tournament_instances/%s/?expand=steps' % saison_uuid
        return self._get_data(journees_url)

    def get_step(self, journee_uuid):
        rencontres_url = '/rest/steps/%s/?expand=meetings' % journee_uuid
        return self._get_data(rencontres_url)

    def get_meeting(self, meeting_uuid):
        meeting_url = '/rest/footballmeetings/%s/' % meeting_uuid
        return self._get_data(meeting_url)

    def get_person_teams(self, person_uuid):
        teams_url = '/rest/football_players/%s/current_teams' % person_uuid
        return self._get_data(teams_url)