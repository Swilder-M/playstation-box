import requests


class PSN:
    npsso: str = None
    access_token: str = None
    refresh_token: str = None
    user_name: str = None
    account_id: str = None
    auth_endpoint = 'https://ca.account.sony.com/api/authz/v3/'
    api_endpoint = 'https://m.np.playstation.com/api/'
    language = 'en-US'

    def __init__(self,
                 npsso: str = None,
                 access_token: str = None,
                 refresh_token: str = None,
                 language: str = None):
        self.npsso = npsso
        self.access_token = access_token
        self.refresh_token = refresh_token

        if language:
            self.language = language

        if not self.check_access_token():
            access_token, refresh_token = self.refresh_access_token()
            if not access_token:
                access_token, refresh_token = self.get_access_token_from_npsso()

            self.access_token = access_token
            self.refresh_token = refresh_token

        if not self.check_access_token():
            raise Exception('Failed to get access token')

    def requester(self, method, api, **kwargs):
        headers = kwargs.get('headers', {})
        if not headers.get('Authorization'):
            headers['Authorization'] = f'Bearer {self.access_token}'
        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'application/json'
        if not headers.get('Accept-Language'):
            headers['Accept-Language'] = self.language
        kwargs['headers'] = headers

        if api.startswith('oauth/'):
            url = self.auth_endpoint + api
        elif api.startswith('userProfile/'):
            url = 'https://us-prof.np.community.playstation.net/' + api
        elif api.startswith('https://') or api.startswith('http://'):
            url = api
        else:
            url = self.api_endpoint + api
        kwargs['url'] = url

        kwargs['method'] = method
        response = requests.request(**kwargs)
        if api.startswith('oauth/') or api.startswith('userProfile/'):
            return response

        if response.status_code >= 400:
            error_message = response.text
            try:
                error_message = response.json()['error']['message']
            except Exception as e:
                pass
            raise Exception(f'Error {method} {api} {response.status_code}: {error_message}')
        return response

    def check_access_token(self):
        if not self.access_token:
            return False
        params = {
            'fields': 'npId,onlineId,accountId,avatarUrls,plus'
        }
        resp = self.requester(method='GET', api='userProfile/v1/users/me/profile2', params=params)
        if resp.status_code == 200:
            record = resp.json()['profile']
            self.user_name = record['onlineId']
            self.account_id = record['accountId']
            return True
        return False

    def refresh_access_token(self):
        if not self.refresh_token:
            return None, None
        data = {
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'psn:mobile.v2.core psn:clientapp',
            'token_format': 'jwt'
        }
        headers = {
            'Authorization': 'Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A=',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        resp = self.requester(method='POST', api='oauth/token', data=data, headers=headers)
        if resp.status_code != 200:
            return None, None
        record = resp.json()
        return record['access_token'], record['refresh_token']

    def get_access_token_from_npsso(self):
        if not self.npsso:
            raise Exception('No npsso code')

        params = {
            'access_type': 'offline',
            'client_id': '09515159-7237-4370-9b40-3806e67c0891',
            'redirect_uri': 'com.scee.psxandroid.scecompcall://redirect',
            'response_type': 'code',
            'scope': 'psn:mobile.v2.core psn:clientapp',
        }
        cookies = {'npsso': self.npsso}
        resp = self.requester(method='GET', api='oauth/authorize',
                              params=params, cookies=cookies, allow_redirects=False)
        if resp.status_code != 302:
            raise Exception('Invalid npsso code')
        code = resp.headers['Location'].split('code=')[1].split('&')[0]

        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'com.scee.psxandroid.scecompcall://redirect',
            'token_format': 'jwt'
        }
        headers = {
            'Authorization': 'Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A=',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        resp = self.requester(method='POST', api='oauth/token', data=data, headers=headers)
        if resp.status_code != 200:
            raise Exception('Failed to get token')
        record = resp.json()
        return record['access_token'], record['refresh_token']

    def game_list(self, offset=0, limit=200):
        resp = self.requester(method='GET', api=f'gamelist/v2/users/me/titles?limit={limit}&offset={offset}')
        if resp.status_code != 200:
            return None

        resp = resp.json()
        games = resp['titles']
        next_offset = resp.get('nextOffset')
        if next_offset:
            games += self.game_list(offset=next_offset)
        return games

    def trophy_list(self, offset=0, limit=500):
        params = {
            'limit': limit,
            'offset': offset,
            'accountId': 'me'
        }
        resp = self.requester(method='GET', api='trophy/v1/users/me/trophyTitles', params=params)
        if resp.status_code != 200:
            return None
        resp = resp.json()
        trophies = resp['trophyTitles']
        next_offset = resp.get('nextOffset')
        if next_offset:
            trophies += self.trophy_list(offset=next_offset)
        return trophies

    def game_trophy_progress(self, game_id):
        params = {
            'accountId': 'me',
            'npTitleIds': game_id
        }
        resp = self.requester(method='GET', api='trophy/v1/users/me/titles/trophyTitles', params=params)
        resp = resp.json()
        for title in resp['titles']:
            if title['npTitleId'] == game_id and title['trophyTitles']:
                return title['trophyTitles'][0]
        return None
