from models.helpers import get_data
import pandas as pd

class Playlist:
    
    FEATURES_LIST = [ 
            'title', 'danceability', 'energy', 'acousticness', 'mode', 'valence',
            'loudness', 'tempo', 'liveness', 'key', 'instrumentalness', 'speechiness', 'likes'
        ]

    def __init__(self, pid, like_flag):
        self.pid = pid
        self.like_flag = like_flag
        self.data = get_data(pid, 'playlists')
    

    # RETURNS list of a feature for all songs in playlist
    # PARAMS features we're looking for
    def get_track_info(self, key):
        return [track['track'][key] for track in self.data['tracks']['items']]


    # RETURNS dataframe w all songs + audio features in the playlist
    def create_df(self):

        # iterate through all track ids and retrieve audio features 
        features = [get_data(track, 'audio-features') for track in self.get_track_info('id')]
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
        tracks = self.data['tracks']
        return [track['track']['artists'][0]['id'] for track in tracks['items']]
