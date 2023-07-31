from models.playlist import Playlist
from models.helpers import BASE_URL, headers, find_top, get_data, get_image
from sklearn.tree import DecisionTreeClassifier
from statistics import mean
import pandas as pd
import requests

##### HELPERS #####

# PARAMS artist_ids: list of artist ids, key: target value
# RETURNS list of key value for each artist
def get_artist_info(artist_ids, key):
    return [get_data(artist, 'artists')[key] for artist in artist_ids]


# PARAM list of artist ids
# RETURNS artist seed for rec
def artist_seeds(artist_ids):
    seed = 'artists='
    for i in artist_ids:
        seed += (i + '%2C')
    return seed[ :-3]

# PARAM list of genres
# RETURNS seed for rec w/ ok genres (0 if not avail)
def genres_seeds(genres):
    r = []
    avail = requests.get(BASE_URL + "recommendations/available-genre-seeds", headers=headers)
    avail = avail.json()
    avail = avail['genres']

    # fixing names
    for g in genres:
        if g == 'alternative rock':
            g = 'alt-rock'
        g.replace(" ", "-")
        if g in avail:
            r.append(g)
    
    if len(r) == 0: # False
        return 0
    
    seed = 'genres='
    for i in r:
        seed += (i + '%2C')
    return seed[ : -3]


class Match(Playlist):

    REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'loudness', 'tempo', 'liveness', 'instrumentalness', 'mode', 'speechiness']
    VERY_REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'liveness', 'instrumentalness', 'speechiness']   

    def __init__(self, pid1y, pid1x, pid2y, pid2x):

        # playlist objects
        self.a = Playlist(pid1y[34 : -20], 1) # user1 likes
        self.b = Playlist(pid1x[34 : -20], 0) # user1 dislikes
        self.c = Playlist(pid2y[34 : -20], 1) # user2 likes
        self.d = Playlist(pid2x[34 : -20], 0) # user2 dislikes

        # dataframes
        self.dfa = self.a.create_df()
        self.dfb = self.b.create_df()
        self.dfc = self.c.create_df()
        self.dfd = self.d.create_df()

        # like playlists' artists + genres, incl repeats
        self.aa = self.a.all_artists()
        self.ac = self.c.all_artists()
        self.ga = self.a.all_genres(self.aa)
        self.gc = self.c.all_genres(self.ac)

    ##### BUBBLES #####

    # RETURNS artist (ids) in both "like" playlists (empty list if none)
    def shared_artists(self): 
        return list(set.intersection(*map(set, [[*set(self.aa)], [*set(self.ac)]])))[ : 5]
    

    # RETURNS names of all shared artists (empty list if nont)
    def shared_artists_names(self):
        return get_artist_info(self.shared_artists(), 'name') if len(self.shared_artists()) != 0 else []


    # RETURNS all shared genres (str)
    def shared_genres(self): 
        return list(set.intersection(*map(set, [[*set(self.ga)], [*set(self.gc)] ])))[ : 5] 


    # RETURNS match's (c) fav artists names (strs)
    def match_fav_artists(self): 
        return get_artist_info(find_top(self.ac, 3), 'name') # return their names

    # RETURNS match's (c) fav genres (strs)
    def match_fav_genres(self):
        return find_top(self.gc, 3)
    

    ##### HEADER #####

    # RETURNS url to playlist image that will be shown in the profile
    def get_match_image(self):
        return get_image(get_data(self.c.pid, 'playlists'))

    # RETURNS compatbility percentage
    # average of DTC's accuracy in predicting whether user 2 will like a song, and its accuracy in predicting whether user1 will like a song
    def find_compatibility(self):
 
        # shorten "dislike" playlists to 525 length of "likes" playlists
        dfb = self.dfb.iloc[0 : int(len(self.dfa.index) / 4)]
        dfd = self.dfd.iloc[0 : int(len(self.dfc.index) / 4)]

        # combine both pl's for each user
        df1 = pd.concat([self.dfa, dfb])
        df2 = pd.concat([self.dfc, dfd])

        X_train = df1[self.REDUCED_FEATURES] # audio features of  user1's songs
        y_train = df1['likes'] # whether user1 (dis) likes a song
        X_test = df2[self.REDUCED_FEATURES] # audio features of user2's songs
        y_test = df2['likes'] # whether user2 will like the song

	    # predict user2 based on user1
        dtc1 = DecisionTreeClassifier()
        dtc1.fit(X_train, y_train) # train on user1
        score1 = dtc1.score(X_test, y_test) # test on user2
        
        # predict user1 based on user1
        dtc2 = DecisionTreeClassifier()
        dtc2.fit(X_test, y_test) # train on user2
        score2 = dtc2.score(X_train, y_train) # test on user1
        return mean([score1, score2])
    

    # RETURNS discretized compatibility (qualitative)
    def comp_desc(self):
        x = self.find_compatibility()
        if x < 0.25:
            return "not compatible"
        elif x < 0.5: 
            return "somewhat incompatible"
        elif x < 0.75:
            return "somewhat compatible"
        else:
            return "compatible"
    
    ##### PROMPTS #####

    # RETURNS dictionary of features where both users are w/in a certain threshold; key = features name, value = mean val
    def find_features(self):
        df = pd.DataFrame(index=range(3), columns=self.VERY_REDUCED_FEATURES)
        for ft in self.VERY_REDUCED_FEATURES:
            df[ft].iloc[0] = mean(self.dfa[ft]) # row 0: mean of each feature for user1
            df[ft].iloc[1] = mean(self.dfc[ft]) # row 1 : same, for user 2
            df[ft].iloc[2] = abs(df[ft].iloc[1] - df[ft].iloc[0]) # row 2: difference for each feature

        # put ft + vals in dict
        ft_list, ft_val = [], []
        cols = df.keys().tolist()
        for i in range(0, len(cols)):
            if df.iloc[2, i] < 0.05:
                ft_list.append(cols[i])
                ft_val.append(mean([df.iloc[0, i], df.iloc[1, i]]))
        return dict(zip(ft_list, ft_val))
    
    ##### ABOUT ME #####

    # RETURNS dict: keys = song names ([title] by [artist]), values = their spotify url
    def recommend_tracks(self):
        
        if len(self.shared_artists()) != 0: # shared artists
            seed = artist_seeds(self.shared_artists())
        elif len(self.shared_genres()) != 0 and genres_seeds(self.shared_genres()) != 0: # shared genres
            seed = genres_seeds(self.shared_genres())
        else: # top 2 artists per user
            seed = artist_seeds(find_top(self.aa, 2) + find_top(self.ac, 2))
        
        for k, v in self.find_features().items():
            seed += ("&target_" + k + "=" + str(v))
        print(seed)
            
        # API call
        data = requests.get(BASE_URL + 'recommendations?limit=4&seed_' + seed, headers=headers)
        data = data.json()

        # get names + urls, return in a dict
        names, urls = [], []

        for track in data['tracks']:
            name = track['name'] + " by " + track['artists'][0]['name']
            names.append(name)
            urls.append(track['external_urls']['spotify'])
        
        return dict(zip(names, urls))


    # RETURNS dict of recommended artists: keys = name, values = url
    def recommend_artists(self):
        # get seed
        if len(self.shared_artists()) != 0:
            artist_ids = self.shared_artists() + find_top(self.ac, 4 - len(self.shared_artists()))
        else:
            artist_ids = find_top(self.aa, 2) + find_top(self.ac, 2)

        # get names + urls, return in a dict
        names, urls = [], []
        for artist_id in artist_ids:
            data = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists', headers=headers)
            data = data.json()
            names.append(data['artists'][0]['name'])
            urls.append(data['artists'][0]['external_urls']['spotify'])

        return dict(zip(names, urls))
  
    
 
    


    
    