import requests
from config import CLIENT_ID, CLIENT_SECRET

########## ACCESS API ##########
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

########## HELPER FUNCTIONS ##########

# PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
# RETURNS json file of object's data
def get_data(item_id, item_type):
	data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
	return data.json()

# PARAMS data: json of all playlist data, key: term/feature we're looking for
# RETURNS list containing values of the key in all tracks
def get_track_info(data, key):
	tracks = data['tracks']
	r = []
	for track in tracks['items']:
		r.append(track['track'][key])
	return r

########## COMPATIBILITY ##########

########## FEATURES ##########
# functions called from app.py

### HEADER ###

# PARAMS item_id: id, item_type: user, album, etc
# RETURNS link to image
def get_image(data):
	images = data['images']
	image = images[0]# first obj in ImageObject array
	return image['url']

### ABOUT ###

# PARAMS ids: list of ids (artist or genre), mode: artist or genre
# RETURNS: list of 5 songs, format "[title] by [artist]"
def recommend(ids, mode):
	seed = '='
	for i in ids:
		seed += (i + '%2C') # add item + comma
	seed = seed[: -3] # remove the last comma'

	data = requests.get(BASE_URL + 'recommendations?limit=5&seed_' + mode + seed, headers=headers)
	data = data.json()

	r = []
	for track in data['tracks']:
		temp = track['name'] + " by " + track['artists'][0]['name']
		r.append(temp)

	return r

### PROMPTS + BUBBLES ###

# PARAMS list1, list2: data to be compared
# RETURNS set of items both playlists have in common
def find_shared(list1, list2):
	r = []
	for i in list1:
		if i in list2 and i not in r:
			r.append(i)
	return r

# PARAM playlist json
# RETURNS list of artists' ids
def artist_ids(data):
	artists = get_track_info(data, 'artists')
	r = []
	for i in artists:
		r.append(i[0]['id'])
	return r

# PARAMS artist_ids: list of artist ids, key: target feature
# RETURNS list of key feature for all artist
def artist_info(artist_ids, key):
	r = []
	for i in artist_ids:
		data = get_data(i, 'artists')
		r.append(data[key])
	return r

# PARAM list of artist ids
# RETURN list of genres (str)
def genres(artist_ids):
	r = []
	for i in artist_ids:
		data = get_data(i, 'artists')
		genres = data['genres']
		if genres[0] not in r:
			r.append(genres[0])
	return r