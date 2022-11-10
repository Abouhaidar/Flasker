import pandas as pd
df=pd.DataFrame(dict(
    name=['John'],
    age=[45],
    location=['London']
))
df.to_csv('users.csv',index=False)