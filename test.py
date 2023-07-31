from models.user import User
from models.playlist import Playlist
from models.match import Match, genres_seeds, get_artist_info
import models.test_data as td
import pandas as pd
from statistics import mean

# uid='kli-17'

# QUIET = td.CLASSICAL
# LOUD = td.PUNK[34 : -20]

#pid1y = td.INDIE[34 : -20]
# pid1x = QUIET

# pid2y = td.ROCK2
# pid2x = QUIET

# m = Match(pid1y, pid2x, pid2y, pid2x)
# x = m.dfa
# print(x)

def haha(df0, df1, df2, df3, df4, ft_list):
    df = pd.DataFrame(index=range(5), columns=ft_list)
    for ft in ft_list:
        df[ft].iloc[0] = mean(df0[ft])
        df[ft].iloc[1] = mean(df1[ft])
        df[ft].iloc[2] = mean(df2[ft])
        df[ft].iloc[3] = mean(df3[ft])
        df[ft].iloc[4] = mean(df4[ft])
    return df
VERY_REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'liveness', 'instrumentalness', 'speechiness', 'tempo', 'loudness']
                         
a = Playlist(td.RAP[34 : -20], 1).create_df()
b = Playlist(td.EDM[34 : -20], 1).create_df()
c = Playlist(td.COUNTRY[34 : -20], 1).create_df()
d = Playlist(td.POP[34 : -20], 1).create_df()
e = Playlist(td.PUNK[34 : -20], 1).create_df()

print(haha(a, b, c, d, e, VERY_REDUCED_FEATURES ))

