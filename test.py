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

p = td.INDIE
q = td.CLASSICAL
m = Match(q, q, p, p)

print(m.find_compatibility())
print(m.comp_desc())