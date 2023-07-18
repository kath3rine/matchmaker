from flask import Flask, request, render_template
from match import get_data, get_image, recommend, shared_artists, artist_info

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

  a = shared_artists(playlist1, playlist2) # shared artist ids

  ##### PROFILE PAGE #####
  # HEADER
  pfp = get_image(user2)
  name = user2['display_name']
  compatibility = '69'# filler value

  # ABOUT
  recs = recommend(a, 'artists')

  # PROMPTS
  s_artists = artist_info(a, 'name') if len(artist_info(a, 'name')) != 0 else 'none :('
  # s_genres = 'shared genres here'
  
  # BUBBLES
  f_artists = 'fav artists here'
  # f_genres = 'fav genres here'

  # render match page
  return render_template('match.html', pfp=pfp, name=name, compatibility=compatibility, 
    recs=recs, len_recs = len(recs), 
    s_artists=s_artists, len_s_artists=len(s_artists),
    f_artists=f_artists, len_f_artists=len(f_artists))

if __name__ == '__main__':
    app.run(debug=True)

