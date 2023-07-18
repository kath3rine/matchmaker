from flask import Flask, request, render_template
from match import get_data, get_track_info, shared_artists, artist_info, get_recs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  user1 = request.form['user1']
  user2 = request.form['user2']
  pl1 = get_data(user1, 'playlists')
  pl2 = get_data(user2, 'playlists')

  shared_a = shared_artists(pl1, pl2)

  # SHARED ARTISTS
  out1 = artist_info(shared_a, 'name')

  # RECOMMENDATIONS
  # TO DO: seed: shared artists -> shared genres (if no shared artists) -> 2 artists per playlist
  out2 = get_recs(shared_a, 'artists')
  return render_template('match.html', out1 = out1, out2=out2)

if __name__ == '__main__':
    app.run(debug=True)

# 2b08l28qJ61zKFztCRrNOl
# 6aTmvWaCEYUOy9xOH5aQ6I