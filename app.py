from flask import Flask, request, render_template
from match import get_data, get_image, recommend, artist_ids, find_shared, artist_info, genres

app = Flask(__name__)

# https://open.spotify.com/user/kli-17?si=dc7771a37b7c480f
# https://open.spotify.com/playlist/2b08l28qJ61zKFztCRrNOl?si=dbc23b7bc7d3480b
# https://open.spotify.com/playlist/6aTmvWaCEYUOy9xOH5aQ6I?si=30540fbdf2b6479e
# https://open.spotify.com/playlist/5t1y9F77hIHGFIUJbdy2PH?si=468e510d221749d8

matches = []

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
  if len(a) != 0: # seed = shared artists
    recs = recommend(a, 'artists')
  elif len(g) != 0: # seed = shared genres
    recs = recommend(g, 'genres')
  else: # seed = first 2 artists from each playlist
    temp = [a1[0], a1[1], a2[0], a2[1]]
    recs = recommend(temp, 'artists')


  # PROMPTS
  s_artists = 'none :(' if len(a) == 0 else artist_info(a, 'name')[ : 5]
  s_genres = 'none :(' if len(g) == 0 else g[ : 5]
  
  # BUBBLES
  f_artists = artist_info(a2, 'name')[ : 5]
  f_genres = g2[ : 5]

  # render match page
  return render_template('match.html', pfp=pfp, name=name, compatibility=compatibility, 
    recs=recs, len_recs = len(recs), 
    s_artists=s_artists, len_s_artists=len(s_artists), 
    s_genres=s_genres, len_s_genres = len(s_genres),
    f_artists=f_artists, len_f_artists=len(f_artists),
    f_genres=f_genres, len_f_genres = len(f_genres))

@app.route('/dislike', methods=['GET', 'POST'])
def dislike():
  return render_template('index.html')

@app.route('/like', methods=['GET', 'POST'])
def like():
  return render_template('index.html')

@app.route('/saved', methods=['GET', 'POST'])
def saved():
  return render_template('saved.html')

if __name__ == '__main__':
    app.run(debug=True)

