from config import BEARER_TOKEN
from TwitterAPI import TwitterAPI
import pandas as pd
from config import *

twitter = TwitterAPI(BEARER_TOKEN=BEARER_TOKEN)

def translate(data):
    data['followers'] = data['public_metrics']['followers_count']
    data['following'] = data['public_metrics']['following_count']
    data['following_ids'] = None
    data.pop('public_metrics')
    return data



# Comenzamos con el primer nodo
maduro_id = 1252764865
res = twitter.get_user(maduro_id)
df = pd.DataFrame.from_dict([ translate(res['data']) ])

# Comenzamos a buscar

user_id = df.iloc[0]['id']
res = twitter.get_user_following(user_id)

data = []
ids = []
for r in res['data']:
    data.append( translate(r) )
    ids.append( str(r['id']) )

df.iloc[0, -1] = ','.join(ids)
df = pd.concat( (df,  pd.DataFrame.from_dict(data)) ).reset_index()

print(df.head())