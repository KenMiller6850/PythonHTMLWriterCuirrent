import pandas as pd
 
def create_df():
    data = {'state': ['Ohio','Ohio','Ohio','Nevada','Nevada'],
           'year': [2000,2001,2002,2001,2002],
           'pop': [1.5,1.7,3.6,2.4,2.9]}
    df = pd.DataFrame(data)
    return df


df = create_df()
print(df)