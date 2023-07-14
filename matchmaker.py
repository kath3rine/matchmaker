import requests

CLIENT_ID='f1b645b681544d408913e0f55784b3a6'
CLIENT_SECRET='a2c5b97a944647d8bce6722c772adbc8'
REDIRECT_URI='http://127.0.0.1:5000/'

def authorize():
	auth_response = requests.post('https://accounts.spotify.com/api/token', {
		'grant_type': 'client_credentials',
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
	})
	auth_response_data = auth_response.json()
	return auth_response_data['access_token']

