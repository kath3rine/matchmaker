from flask import Flask, request, render_template
from match import get_data, get_image, recommend, artist_ids, find_shared, artist_info, genres

app = Flask(__name__)

# https://open.spotify.com/user/kli-17?si=dc7771a37b7c480f
# https://open.spotify.com/playlist/2b08l28qJ61zKFztCRrNOl?si=dbc23b7bc7d3480b
# https://open.spotify.com/playlist/6aTmvWaCEYUOy9xOH5aQ6I?si=30540fbdf2b6479e

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  
  # get urls/ids
  uid1 = request.form['user1']
  uid2 = request.form['user2']
  pid1 = request.form['playlist1']
  pid2 = request.form['playlist2']
  pid1, pid2 = pid1[34 : -20], pid2[34 : -20]

  # create jsons of data
  user1, user2 = get_data(uid1, 'users'), get_data(uid2, 'users') 
  playlist1, playlist2 = get_data(pid1, 'playlists'), get_data(pid2, 'playlists')

  # get artists and genres
  a1, a2 = artist_ids(playlist1), artist_ids(playlist2) 
  a = find_shared(a1, a2) 
  g1, g2 = genres(a1), genres(a2)
  g = find_shared(g1, g2)

  ##### PROFILE PAGE #####
  # HEADER
  pfp = get_image(user2)
  name = user2['display_name']
  compatibility = '69'# filler value

  # ABOUT
  recs = recommend(a, 'artists')

  # PROMPTS
  s_artists = artist_info(a, 'name') if len(artist_info(a, 'name')) != 0 else 'none :('
  
  # BUBBLES
  f_artists = artist_info(a2, 'name')

  # render match page
  return render_template('match.html', pfp=pfp, name=name, compatibility=compatibility, 
    recs=recs, len_recs = len(recs), 
    s_artists=s_artists, len_s_artists=len(s_artists), 
    s_genres=g, len_s_genres = len(g),
    f_artists=f_artists, len_f_artists=len(f_artists),
    f_genres=g2, len_f_genres = len(g2))

if __name__ == '__main__':
    app.run(debug=True)

