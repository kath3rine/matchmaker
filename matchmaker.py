import app 
import logging, requests, time

def getToken(code):
	token_url = 'https://accounts.spotify.com/api/token'
	authorization = app.config['AUTHORIZATION']
	redirect_uri = app.config['REDIRECT_URI']

	headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'code': code, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
	post_response = requests.post(token_url, headers=headers, data=body)

	# 200 code indicates access token was properly granted
	if post_response.status_code == 200:
		json = post_response.json()
		return json['access_token'], json['refresh_token'], json['expires_in']
	else:
		logging.error('getToken:' + str(post_response.status_code))
		return None

def makeGetRequest(session, url, params={}):
  headers = {"Authorization": "Bearer {}".format(session['token'])}
  response = requests.get(url, headers=headers, params=params)
  if response.status_code == 200:
    return response.json()
  elif response.status_code == 401 and checkTokenStatus(session) != None:
    return makeGetRequest(session, url, params)
  else:
    logging.error('makeGetRequest:' + str(response.status_code))
    return None

def checkTokenStatus(session):
  if time.time() > session['token_expiration']:
    payload = refreshToken(session['refresh_token'])
  if payload != None:
    session['token'] = payload[0]
    session['token_expiration'] = time.time() + payload[1]
  else:
    logging.error('checkTokenStatus')
    return None
  return "Success"

def refreshToken(refresh_token):
	token_url = 'https://accounts.spotify.com/api/token'
	authorization = app.config['AUTHORIZATION']

	headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
	post_response = requests.post(token_url, headers=headers, data=body)

	# 200 code indicates access token was properly granted
	if post_response.status_code == 200:
		return post_response.json()['access_token'], post_response.json()['expires_in']
	else:
		logging.error('refreshToken:' + str(post_response.status_code))
		return None