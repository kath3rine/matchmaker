from helpers import get_data
import pandas as pd

class Playlist:
    
    FEATURES_LIST = [ 
            'title', 'danceability', 'energy', 'acousticness', 'mode', 'valence',
            'loudness', 'tempo', 'liveness', 'key', 'instrumentalness', 'likes'
        ]

    def __init__(self, pid, like_flag):
        self.pid = pid
        self.like_flag = like_flag
        self.data = get_data(pid, 'playlists')
    

    # RETURNS list of a feature for all songs in playlist
    # PARAMS features we're looking for
    def get_track_info(self, key):
        r = []
        data = self.data
        tracks = data['tracks']
        for track in tracks['items']:
            r.append(track['track'][key])
        return r


    # RETURNS dataframe w all songs + audio features in the playlist
    def create_df(self):

        # iterate through all tracks and retrieve audio features 
        features = [] # list of dicts, 1 per song
        track_ids = self.get_track_info('id')
        for track in track_ids:
            data = get_data(track, 'audio-features')
            features.append(data)

        df = pd.DataFrame(data=features, columns=features[0].keys())

        likes = []
        for i in range(0, len(df.index)):
            likes.append(0) if self.like_flag == 0 else likes.append(1)
        
        df['likes'] = likes
        df['title'] = self.get_track_info('name')

        return df[self.FEATURES_LIST]
    

    # RETURNS list of all genres, w/ repeats (str)
    def all_genres(self, artist_ids):
        r = []
        for i in artist_ids:
            data = get_data(i, 'artists')
            if len(data['genres']) > 0:
                r.append(data['genres'][0])

        return r

    # RETURNS list of all artist ids in playlist, incl repeats
    def all_artists(self):
        r = []
        tracks = self.data['tracks']
        for track in tracks['items']:
            r.append(track['track']['artists'][0]['id'])
        return r