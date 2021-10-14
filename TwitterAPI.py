import requests

class TwitterAPI:

    def __init__(self, BEARER_TOKEN):
        self.PATH = 'https://api.twitter.com/2'
        self.BEARER_TOKEN = BEARER_TOKEN
        self.headers =  {"Authorization": f"Bearer {BEARER_TOKEN}"}

    def get_user(self, user_id):
        params = { 'user.fields':'public_metrics' }
        res = requests.get(f'{self.PATH}/users/{user_id}', params=params, headers=self.headers)
        return res.json()

    def get_user_followers(self, user_id, max_results=1000):
        params = { 'max_results':max_results, 'user.fields':'public_metrics' }
        res = requests.get(f'{self.PATH}/users/{user_id}/followers', params=params, headers=self.headers)
        return res.json()

    def get_user_following(self, user_id, max_results=1000):
        params = { 'max_results':max_results, 'user.fields':'public_metrics' }
        res = requests.get(f'{self.PATH}/users/{user_id}/following', params=params, headers=self.headers)
        return res.json()