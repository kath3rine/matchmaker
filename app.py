from flask import Flask, request, render_template
from match import matchmaker

app = Flask(__name__)

matches = [] # list of profiles user1 has "matched" with thus far
matches_pfp = [] # list of matches' pfp

# HOMEPAGE (input data/"disliked' redirect")
@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('index.html')

# MATCH (user2's profile + stats)
@app.route('/match', methods=["GET", "POST"])
def match():
  
  # get urls/ids
  pid1y = request.form['input1']
  pid1x =  request.form['input2']
  pid2 = request.form['input3']
  uid = request.form['input4']

  m = matchmaker(pid1y, pid1x, pid2, uid)

  # render match page
  return render_template ('match.html', 
    pfp = m['pfp'], name = m['name'], 
    compatibility = str(m['compatibility'])[ : 5], 
    sim_features = m['sim_features'], 
    s_artists = m['s_artists'], s_genres = m['s_genres'], 
    f_artists = m['f_artists'], f_genres = m['f_genres'],
    rec_tracks_names = m['rec_tracks_names'], 
    rec_tracks_urls = m['rec_tracks_urls'],
    rec_artists_names = m['rec_artists_names'], 
    rec_artists_urls = m['rec_artists_urls'])

# LIKE A MATCH (add to queue)
@app.route('/like', methods=['GET', 'POST'])
def like():
  match_name = request.form['name-here']
  match_pfp = request.form['pfp-here']
  global matches
  matches.append(match_name)
  global matches_pfp
  matches_pfp.append(match_pfp)
  return render_template('index.html')

# VIEW YOUR MATCHES
@app.route('/saved', methods=['GET', 'POST'])
def saved():
  return render_template('saved.html', matches=matches, matches_pfp=matches_pfp, len_matches=len(matches))

if __name__ == '__main__':
    app.run(debug=True)

