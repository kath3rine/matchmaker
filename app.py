from flask import Flask, request, render_template
from user import User
from match import Match
import test_data as td

app = Flask(__name__)

# GLOBAL vars: info abt matched users
matches, matches_pfp, matches_urls = [], [], []


# HOMEPAGE (input data/"disliked' redirect")
@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('index.html')


@app.route('/match', methods=["GET", "POST"])
def match():

    QUIET = td.CLASSICAL
    LOUD = td.ROCK2
   # get urls/ids
    pid1y = request.form['input1']
    pid2y = request.form['input3']
    uid = request.form['input5']

    pid1x=LOUD if request.form['dislikes1'] == 'dislike1-option1' else QUIET
    pid2x=LOUD if request.form['dislikes2'] == 'dislike2-option1' else QUIET

    u = User(uid)
    m = Match(pid1y, pid1x, pid2y, pid2x)

    rec_tracks = m.recommend_tracks()
    rec_artists = m.recommend_artists()

    return render_template('match.html',
        name=u.name,
        pfp = m.get_match_image(),
        compatibility = str(m.find_compatibility() * 100)[ : 5],
        user_pfp = u.pfp,
        user_url = u.url,
        rec_tracks_names = list(rec_tracks.keys()),
        rec_tracks_urls = list(rec_tracks.values()),
        rec_artists_names = list(rec_artists.keys()),
        rec_artists_urls = list(rec_artists.values()),
        sim_features = str(list(m.find_features().keys()))[1 : -1],
        s_artists = m.shared_artists_names(),
        f_artists = m.match_fav_artists(),
        s_genres = m.shared_genres(),
        f_genres = m.match_fav_genres(),
    )



# LIKE A MATCH (add to queue)
@app.route('/like', methods=['GET', 'POST'])
def like():

    match_name = request.form['name-here']
    match_pfp = request.form['pfp-here']
    match_url = request.form['url-here']

    global matches
    matches.append(match_name)
    global matches_pfp
    matches_pfp.append(match_pfp)
    global matches_urls
    matches_urls.append(match_url)

    return render_template('index.html')


# VIEW YOUR MATCHES
@app.route('/saved', methods=['GET', 'POST'])
def saved():
  return render_template('saved.html', 
      matches=matches, matches_pfp=matches_pfp, len_matches=len(matches))

if __name__ == '__main__':
    app.run(debug=True)