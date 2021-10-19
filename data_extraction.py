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

def next_level(df, last_level=False):
    df = df.copy()
    
    i=0
    for idx in df[df.following_ids.isnull()].index:
        res = twitter.get_user_following(idx)
        
        data = []
        ids = []
        for r in res:
            data.append( translate(r) )
            ids.append( str(r['id']) )
        
        df.loc[idx, 'following_ids'] = ','.join(ids)
        
        if not last_level:
            new_df = pd.DataFrame.from_dict(data).set_index('id')
            new_ids = set(new_df.index) - set(df.index)
            df = df.append(new_df.loc[new_ids])
        
        if i % 5 == 0:
            df.to_csv('./dataset/checkpoint.csv')
        i += 1
    
    return df

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

# df = pd.DataFrame.from_dict([ translate(twitter.get_user(n)['data']) for n in starting_nodes]).set_index('id')

# df = next_level(df)
# df.to_csv('./dataset/first_level.csv')

# lower_cutoff = df[df.followers < 1e6].followers.quantile(0.90) # Tomaremos el 15% con mas seguidores
# upper_cutoff = 7200000 # No tomaremos los mayores a Capriles, no hay nada interesante
# df = df[(df.followers > lower_cutoff) & (df.followers < upper_cutoff)]
# last_df = next_level(df, last_level=True)
#last_df.to_csv('./dataset/last_checkpoint.csv')

# Continuamos la lista en el ultimo checkpoint
df = pd.read_csv('./dataset/checkpoint_clean.csv', index_col='id')
last_df = next_level(df, last_level=True)
last_df.to_csv('./dataset/last_checkpoint.csv')