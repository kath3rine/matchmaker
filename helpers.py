from secret import CLIENT_ID, CLIENT_SECRET
import requests

BASE_URL = 'https://api.spotify.com/v1/'

def authorize():
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
        
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

access_token = authorize()
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


def get_data(item_id, item_type):
     # PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
    # RETURNS json file of object's data

    data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
    return data.json()

def get_image(data):
    # PARAMS data: json of obj info
    # RETURNS link to image

    image = data['images'][0]
    return image['url']

def find_top(lst, n):
    r = []
    for i in range (0, n):
        x = max(set(lst), key = lst.count)
        r.append(x)
        lst = list(filter((x).__ne__, lst))
    return r

def contains_space(x):
	# PARAM list of strs
	# RETURNS whether any element in that list has a space in it
        for i in x:
            if " " in i:
                return True
        return False

def get_artist_info(artist_ids, key):
	# PARAMS artist_ids: list of artist ids, key: target value
	# RETURNS list of key value for each artist

	r = []
	for artist in artist_ids:
		data = get_data(artist, 'artists')
		r.append(data[key])
	return r


