from flask import Flask, request, render_template
from matchmaker import authorize

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  user1 = request.form['user1']
  user2 = request.form['user2']
  access_token = authorize()
  out = access_token
  return render_template('match.html', out=out)

if __name__ == '__main__':
    app.run(debug=True)
