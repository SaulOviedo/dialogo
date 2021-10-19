import requests
import time

class TwitterAPI:

    def __init__(self, BEARER_TOKEN):
        self.PATH = 'https://api.twitter.com/2'
        self.BEARER_TOKEN = BEARER_TOKEN
        self.headers =  {"Authorization": f"Bearer {BEARER_TOKEN}"}

    def get_user(self, user_id):
        params = { 'user.fields':'public_metrics,profile_image_url' }
        res = requests.get(f'{self.PATH}/users/{user_id}', params=params, headers=self.headers)
        return res.json()

    def get_user_followers(self, user_id, max_results=1000):
        params = { 'max_results':max_results, 'user.fields':'public_metrics,profile_image_url' }
        data = []
        next_token = True

        i = 0
        while next_token and i < 10:
            res = requests.get(f'{self.PATH}/users/{user_id}/followers', params=params, headers=self.headers)
            data += res.json()['data']
            next_token = res.json()['meta'].get('next_token')
            params['pagination_token'] = next_token
            i += 1
        return data

    def get_user_following(self, user_id, max_results=1000):
        params = { 'max_results':max_results, 'user.fields':'public_metrics,profile_image_url' }
        data = []
        next_token = True

        i = 0
        while next_token and i < 10:
            try:
                res = requests.get(f'{self.PATH}/users/{user_id}/following', params=params, headers=self.headers)
                if res.status_code != 200:
                    print('Taking a nap...')
                    time.sleep( 15*60  + 10) # Sleep 15 mins and 10 seconds
                    print('Waking up again!')
                else:
                    data += res.json()['data']
                    next_token = res.json()['meta'].get('next_token')
                    params['pagination_token'] = next_token
                    i += 1
            except Exception as e:
                print('There was an error! Taking a nap...')
                print(e)
                time.sleep(60) # Sleep 15 mins and 10 seconds
                print('Waking up again!')
        return data