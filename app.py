from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  user1 = request.form['user1']
  user2 = request.form['user2']
  return render_template('match.html', user1=user1, user2=user2)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/authorize')
def authorize():
  client_id = app.config['CLIENT_ID']
  redirect_uri = app.config['REDIRECT_URI']
  scope = app.config['SCOPE']

  authorize_url = 'https://accounts.spotify.com/en/authorize?'
  parameters = 'response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scope
  response = make_response(redirect(authorize_url + parameters))
  return response
