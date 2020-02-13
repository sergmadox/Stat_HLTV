import pandas as pd
import numpy as np
import collections

data = pd.read_csv('player_ind_stat.csv')


print (data.head())
nick_names = data['headshot'].toList()

print (nick_names)

