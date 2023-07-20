import requests
from config import CLIENT_ID, CLIENT_SECRET

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

# PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
# RETURNS json file of object's data
def get_data(item_id, item_type):
	data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
	return data.json()

# PARAMS data: json of all playlist data, key: target feature
# RETURNS list of track info
def get_track_info(data, key):
	r = []
	tracks = data['tracks']
	for track in tracks['items']:
		r.append(track['track'][key])
	return r

# PARAM list of track ids
# RETURNS list of dicts containing audio features (1 elem / song)
def get_audio_features(track_ids):
	r = []
	for track in track_ids:
		data = get_data(track, 'audio-features')
		r.append(data)
	return r


# PARAM list of track ids
# RETURNS list of artists' ids
def get_artist_info(data, key):
	r = []
	tracks = data['tracks']
	for track in tracks['items']:
		r.append(track['track']['artists'][0][key])
	return r

# PARAMS ids: list of ids (artist, track etc), key: target features
# RETURNS list of target feature values
def get_value(ids, key):
	r = []
	for i in ids:
		r.append(i[key])
	return r

# PARAMS item_id: id, item_type: user, album, etc
# RETURNS link to image
def get_image(data):
	images = data['images']
	image = images[0]# first obj in ImageObject array
	return image['url']

# PARAM list of artist ids
# RETURN list of genres (str)
def get_genres(artist_ids):
	r = []
	for i in artist_ids:
		data = get_data(i, 'artists')
		genres = data['genres']
		if genres[0] not in r:
			r.append(genres[0])
	return r

# PARAMS ids: list of ids (artist or genre), mode: artist or genre
# RETURNS: list of 5 songs, format "[title] by [artist]"
def recommend_tracks(ids, mode):
	seed = '='
	for i in ids:
		seed += (i + '%2C') # add item + comma
	seed = seed[: -3] # remove the last comma'

	data = requests.get(BASE_URL + 'recommendations?limit=3&seed_' + mode + seed, headers=headers)
	data = data.json()

	r = []
	for track in data['tracks']:
		temp = track['name'] + " by " + track['artists'][0]['name']
		r.append(temp)

	return r

def recommend_artists(artist_ids):
	r = []
	for artist in artist_ids:
		data = requests.get(BASE_URL + 'artists/' + artist + '/related-artists')
		data = data.json()
		a = data['artists'][0]
		if a['name'] not in r:
			r.append(a['name'])
	return


# PARAMS list1, list2: data to be compared
# RETURNS set of items both playlists have in common
def find_shared(list1, list2):
	r = []
	for i in list1:
		if i in list2 and i not in r:
			r.append(i)
	return r

