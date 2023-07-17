from flask import Flask, request, render_template
from match import shared_artists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  user1 = request.form['user1']
  user2 = request.form['user2']
  out = shared_artists(user1, user2, 'name')
  return render_template('match.html', out=out)

if __name__ == '__main__':
    app.run(debug=True)