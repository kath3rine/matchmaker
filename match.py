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

# PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
# RETURNS json file of all playlist data
def get_data(item_id, item_type):
	data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
	return data.json()

# PARAMS data: json of all playlist data; key: term/feature we're looking for
# RETURNS list containing values of the key in all tracks
def get_track_info(data, key):
	tracks = data['tracks']
	r = []
	for track in tracks['items']:
		r.append(track['track'][key])
	return r

# PARAM: artist: list of artist objects, key: target feature (either name or id)
# RETURNS: list of artist ids 
def get_artist_ids(artists):
	r = []
	for i in artists:
		r.append(i[0]['id'])
	return r

# RETURNS audio features of a song
def track_features(track_id):
	features = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
	return features.json()

# PARAMS list1, list2: input data to be compared
# RETURNS set of items both playlists have in common
def find_shared(list1, list2):
	r = []
	for i in list1:
		if i in list2 and i not in r:
			r.append(i)
	return r

##### FEATURES #####

# PARAMS data1, data2: jsons of data from each playlist
# RETURNS list of shared artists' ids
def shared_artists(data1, data2):
	artists1, artists2 = get_track_info(data1, 'artists'), get_track_info(data2, 'artists')
	artist_ids1, artist_ids2 = get_artist_ids(artists1), get_artist_ids(artists2)
	return find_shared(artist_ids1, artist_ids2)

# PARAMS artist_ids: list of artist ids, key: target feature
# RETURNS list of key feature for all artis
def artist_info(artist_ids, key):
	r = []
	for i in artist_ids:
		data = get_data(i, 'artists')
		r.append(data[key])
	return r

# PARAMS ids: list of ids (artist or genre), mode: artist or genre
def get_recs(ids, mode):
	seed = '='
	for i in ids:
		seed += i
		seed += '%2C'# comma separator after each id
	seed = seed[:-3] # remove the last '%2C'

	data = requests.get(BASE_URL + 'recommendations?limit=5&seed_' + mode + seed, headers=headers)
	data = data.json()

	r = []
	for track in data['tracks']:
		temp = track['name'] + " by " + track['artists'][0]['name']
		r.append(temp)

	return r
