import requests
import pandas as pd
from statistics import mean
from sklearn.tree import DecisionTreeClassifier
from secret import CLIENT_ID, CLIENT_SECRET

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

########## GET DATA ##########

BASE_URL = 'https://api.spotify.com/v1/'

def get_data(item_id, item_type):
	# PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
	# RETURNS json file of object's data

	data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
	return data.json()

def get_track_info(data, key):
	# PARAMS data: json of all playlist data, key: target feature
	# RETURNS list of track info

	r = []
	tracks = data['tracks']
	for track in tracks['items']:
		r.append(track['track'][key])
	return r


def get_audio_features(track_ids):
	# PARAM list of track ids
	# RETURNS list of dicts containing audio features (1 elem / song)
	
	r = []
	for track in track_ids:
		data = get_data(track, 'audio-features')
		r.append(data)
	return r

def get_all_artist_info(data, key):
	# PARAM data: json of playlist data, key: target features
	# RETURNS list of artists' key info (w/ dupes)

	r = []
	tracks = data['tracks']
	for track in tracks['items']:
		r.append(track['track']['artists'][0][key])
	return r

def get_image(data):
	# PARAMS data: json of obj info
	# RETURNS link to image

	image = data['images'][0]
	return image['url']

def get_genres(artist_ids):
	# PARAM list of artist ids
	# RETURN list of genres, w/ repeats (str)

	r = []
	for i in artist_ids:
		data = get_data(i, 'artists')
		genre = data['genres'][0]
		if genre is None:
			continue
		else: 
			r.append(genre)
	return r


def get_artist_info(artist_ids, key):
	# PARAMS artist_ids: list of artist ids, key: target value
	# RETURNS list of key value for each artist

	r = []
	for artist in artist_ids:
		data = get_data(artist, 'artists')
		r.append(data[key])
	return r


########## FIND (bubbles + prompts) ##########

def find_shared(lsts):
	# PARAMS list of lists 
	# RETURN elements included in all lists (w/o dupes)

	return list(set.intersection(*map(set, lsts)))

def find_top(lst, n):
	# PARAMS lst: input list, n: number of elements to extract
	# RETURNS n elements that appear the most often

    r = []
    for i in range (0, n):
        x = max(set(lst), key = lst.count)
        r.append(x)
        lst = list(filter((x).__ne__, lst))
    return r

def find_features(df1, df2, FEATURES):
	df = pd.DataFrame(index=range(3), columns=FEATURES)
	for ft in FEATURES:
		df[ft].iloc[0] = mean(df1[ft]) # row 0: mean of each feature for user1
		df[ft].iloc[1] = mean(df2[ft]) # row 1 : same, for user 2
		df[ft].iloc[2] = abs(df[ft].iloc[1] - df[ft].iloc[0]) # row 2: difference for each feature

	r = []
	cols = df.keys().tolist()
	for i in range(0, len(cols)):
		if df.iloc[2, i] < 0.05:
			r.append(cols[i])
	return r


########## RECOMMEND ("about") ##########

def recommend_tracks(ids, mode):
	# PARAMS ids: list of ids (artist or genre), mode: artist or genre
	# RETURNS: list of 5 songs, format "[title] by [artist]"

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
	# PARAMS artist_ids: list of artist ids
	# RETURNS related artists (1 per artist in param)

	r = []
	for artist in artist_ids:
		data = requests.get(BASE_URL + 'artists/' + artist + '/related-artists', headers=headers)
		data = data.json()
		a = data['artists'][0]
		r.append(a['name'])
	return [*set(r)]


##### COMPATIBILITY ("age") #####

def create_df(pid, like_flag):
	# PARAMS pid: playlist id, like_flag: whether songs are liked or disliked
	# RETURNS dataframe w/ all features in a playlist

	FEATURES_LIST = ['track_titles', 'artist_ids', 'artist_name', 
	'danceability', 'energy', 'acousticness', 'mode', 'valence',
	'loudness', 'tempo', 'liveness', 'key', 'instrumentalness', 'likes']

	pl = get_data(pid, 'playlists')
	track_ids = get_track_info(pl, 'id')
	track_titles = get_track_info(pl, 'name')
	artist_ids = get_all_artist_info(pl, 'id')
	artist_names = get_all_artist_info(pl, 'name')

	features = get_audio_features(track_ids)
	df = pd.DataFrame(data=features, columns=features[0].keys())

	likes = []
	for i in range(0, len(df.index)):
		likes.append(0) if like_flag == 0 else likes.append(1)
    
	df['track_titles'] = track_titles
	df['artist_name'] = artist_names
	df['artist_ids'] = artist_ids
	df['likes'] = likes

	return df[FEATURES_LIST]

def combine_df(df_lst):
	# PARAM list of dataframes to be concatenated
	# RETURNS concatenated df
	return pd.concat(df_lst)

def find_compatibility(X_train, y_train, X_test, y_test):
	# PARAMS
	# X_train: audio features of user1's songs
	# y_train: whether user1 (dis)likes a song
	# X_test: audio features of user2's liked songs
	# y_test: whether user2 will like the song

	# RETURNS compatbility percentage, i.e. DTC's accuracy in predicting whether user 2 will like a song

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    return dtc.score(X_test, y_test)



