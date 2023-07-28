from user import User
from playlist import Playlist
from match import Match
import test_data as td

uid='kli-17'

QUIET = td.CLASSICAL
LOUD = td.ROCK2

pid1y = td.INDIEROCK
pid1x = QUIET

pid2y = td.ROCK2
pid2x = QUIET

m = Match(pid1y, pid2x, pid2y, pid2x)
x = m.dfa
print(x)