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
starting_nodes = [
    1252764865, # Nicolas Maduro
    128262354, # Diosdado Cabello
    1644228493, # Delcy Rodriguez
    109601997, # Jorge Rodríguez
    39176902, # Juan Guaido
    14119371, # Julio Borges
    42434332, # Leopoldo Lopez
    47491330, # Henrique Capriles
]

res = twitter.get_user(starting_nodes[4])
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
df = pd.concat( (df,  pd.DataFrame.from_dict(data)) ).set_index('id')

print(df.head(50))