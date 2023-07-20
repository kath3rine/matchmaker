from flask import Flask, request, render_template
from match import matchmaker

app = Flask(__name__)

matches = []

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('index.html')

@app.route('/match', methods=["GET", "POST"])
def match():
  
  # get urls/ids
  pid1y = request.form['input1']
  pid1x =  request.form['input2']
  pid2 = request.form['input3']
  uid = request.form['input4']

  out = matchmaker(pid1y, pid1x, pid2, uid)
  
  # render match page
  return render_template('match.html', out=out)

@app.route('/like', methods=['GET', 'POST'])
def like():
  x = request.form['name-here']
  global matches
  matches.append(x)
  return render_template('index.html')

@app.route('/saved', methods=['GET', 'POST'])
def saved():
  return render_template('saved.html', out=matches)

if __name__ == '__main__':
    app.run(debug=True)

