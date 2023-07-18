from flask import Flask, request, render_template
from match import get_data, shared_artists, artist_info

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
  shared = shared_artists(pl1, pl2)
  out = artist_info(shared, 'name')
  return render_template('match.html', out=out)

if __name__ == '__main__':
    app.run(debug=True)