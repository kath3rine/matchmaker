from playlist import Playlist
from helpers import BASE_URL, headers, find_top, get_image, get_data, contains_space, get_artist_info
from sklearn.tree import DecisionTreeClassifier
from statistics import mean
import pandas as pd
import requests

##### HELPERS #####

class Match(Playlist):

    REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'loudness', 'tempo', 'liveness', 'instrumentalness', 'mode']
    VERY_REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'liveness', 'instrumentalness']   

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
        x, y = [*set(self.aa)], [*set(self.ac)] # rm dupes
        return list(set.intersection(*map(set, [x, y])))
    

    # RETURNS names of all shared artists (empty list if nont)
    def shared_artists_names(self):
        x = self.shared_artists()
        return get_artist_info(x, 'name') if len(x) != 0 else []


    # RETURNS all shared genres (str)
    def shared_genres(self): 
        x, y = [*set(self.ga)], [*set(self.gc)] # rm
        return list(set.intersection(*map(set, [x, y]))) 


    # RETURNS match's (c) fav artists names (strs)
    def match_fav_artists(self): 
        x = find_top(self.ac, 3) # top 3 artist ids
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
 
        # shorten "dislike" playlists to 50% length of "likes" playlists
        dfb = self.dfb.iloc[0 : int(len(self.dfa.index) / 2)]
        dfd = self.dfd.iloc[0 : int(len(self.dfc.index) / 2)]

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
                x, y = df.iloc[0, i], df.iloc[1, i]
                ft_val.append(mean([x, y]))
        return dict(zip(ft_list, ft_val))
    
    ##### ABOUT ME #####

    # RETURNS dict: keys = song names ([title] by [artist]), values = their spotify url
    def recommend_tracks(self):
        
        if len(self.shared_artists()) != 0: # shared artists
            ids = self.shared_artists()
            mode = 'artists'
        elif len(self.shared_genres()) != 0 and contains_space(self.shared_genres()) is False: # shared genres
            ids = self.shared_genres()
            mode = 'genres'
        else: # top 2 artists per user
            ids = find_top(self.aa, 2) + find_top(self.ac, 2)
            mode='artists'
        
        # generate seed (artist/genre + sim feat, if any)
        seed = '='
        for i in ids:
            seed += (i + '%2C')
        seed = seed[: -3] # remove the last comma
        for k, v in self.find_features().items():
            seed += ("&target_" + k + "=" + str(v))
            
        # API call
        data = requests.get(BASE_URL + 'recommendations?limit=4&seed_' + mode + seed, headers=headers)
        data = data.json()

        # get names + urls, return in a dict
        names, urls = [], []

        for track in data['tracks']:
            name = track['name'] + " by " + track['artists'][0]['name']
            names.append(name)
            temp = track['external_urls']
            urls.append(temp['spotify'])
        

        return dict(zip(names, urls))


    # RETURNS dict of recommended artists: keys = name, values = url
    def recommend_artists(self):
        # get seed
        if len(self.shared_artists()) != 0:
            artist_ids = self.shared_artists()
        else:
            artist_ids = find_top(self.aa, 2) + find_top(self.ac, 2)

        # get names + urls, return in a dict
        names, urls = [], []
        for artist_id in artist_ids:
            data = requests.get(BASE_URL + 'artists/' + artist_id + '/related-artists', headers=headers)
            data = data.json()
            a = data['artists'][0] 
            names.append(a['name'])
            b = a['external_urls']
            urls.append(b['spotify'])

        return dict(zip(names, urls))
  
    
 
    


    
    