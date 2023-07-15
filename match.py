import requests
import pandas as pd

CLIENT_ID='f1b645b681544d408913e0f55784b3a6'
CLIENT_SECRET='a2c5b97a944647d8bce6722c772adbc8'
REDIRECT_URI='http://127.0.0.1:5000/'
BASE_URL = 'https://api.spotify.com/v1/'

def authorize():
	auth_response = requests.post('https://accounts.spotify.com/api/token', {
		'grant_type': 'client_credentials',
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
	})
	auth_response_data = auth_response.json()
	return auth_response_data['access_token']

access_token = authorize()
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# FETCH DATA FROM API
def get_track(playlist):
	r = requests.get(BASE_URL + 'playlists/' + playlist, headers=headers )
	r = r.json()
	lst = r['tracks']
	ret = []
	for track in lst['items']:
		ret.append(track['track']['name'])
	return ret

def track_info(track_id):
	r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
	r = r.json()
	return r['danceability']