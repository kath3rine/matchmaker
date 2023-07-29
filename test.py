from models.user import User
from models.playlist import Playlist
from models.match import Match, genres_seeds, get_artist_info
import models.test_data as td

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
PL = td.FAV
PL2 = td.RAP
PP = td.CLASSICAL

m = Match(PL, PP, PL2, PP)
print(m.find_compatibility())
print(m.find_features())