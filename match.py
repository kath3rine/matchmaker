import requests
# import pandas as pd

##### ACCESS API #####

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

##### HELPER FUNCTIONS #####

# RETURNS json file of all playlist data
def get_data(playlist_id):
	playlist = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers )
	return playlist.json()

# PARAMS data: json of all playlist data; key: term/feature we're looking for
# RETURNS list containing values of the key in all tracks
def get_info(data, key):
	tracks = data['tracks']
	l = []
	for track in tracks['items']:
		l.append(track['track'][key])
	return l

# PARAM: artist: list of artist objects, key: target feature (either name or id)
# RETURNS: list of artist names (str)
def get_artist(artists, key):
	l = []
	for i in artists:
		l.append(i[0][key])
	return l

# RETURNS audio features of a song
def track_features(track_id):
	features = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
	return features.json()

# PARAMS list1, list2: input data to be compared
# RETURNS set of items both playlists have in common
def find_shared(list1, list2):
	l = []
	for i in list1:
		if i in list2 and i not in l:
			l.append(i)
	return l

##### FEATURES #####

# PARAMS user1, user2: each user's playlist id, key: target feature (id or name)
# RETURNS list of artists in both playlists (either their ids or names)
def shared_artists(user1, user2, key):
	data1, data2 = get_data(user1), get_data(user2)
	artists1, artists2 = get_artist(get_info(data1, 'artists'), key), get_artist(get_info(data2, 'artists'), key) 
	return find_shared(artists1, artists2)


