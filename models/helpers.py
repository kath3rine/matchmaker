from models.secret import CLIENT_ID, CLIENT_SECRET
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


# PARAMS item_id: id of object, item_type: type of object (artist, playlist, etc)
# RETURNS json file of object's data
def get_data(item_id, item_type):
    data = requests.get(BASE_URL + item_type + '/' + item_id, headers=headers )
    return data.json()


# RETURNS top #n most common elements
def find_top(lst, n):
    r = []
    for i in range (0, n):
        x = max(set(lst), key = lst.count)
        r.append(x)
        lst = list(filter((x).__ne__, lst))
    return r

def get_image(data):
    return data['images'][0]['url']


