from helpers import get_image, get_artist_info, get_data, get_genres, create_df, find_compatibility, find_top, find_shared, find_features, recommend_artists, recommend_tracks, recommend_track_names, recommend_track_urls, combine_df

def matchmaker(pid1y, pid1x, pid2, uid):
    # PARAMS 
    # pid1, pid1x, pid2: playlist urls of songs user1 likes, user1 dislikes, and user2 likes, respectively
    # uid: user2's id

    # RETURNS
    # dict: keys = variables/features, values = value

    # constants
    REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'loudness', 'tempo', 'liveness', 'instrumentalness', 'mode']
    VERY_REDUCED_FEATURES = ['danceability', 'energy', 'acousticness', 'valence', 'liveness', 'instrumentalness']

    # initialize dictionary of features to return
    var_list = ['pfp', 'name', 'compatibility', # header
                'sim_features', # prompts
                's_artists', 's_genres', 'f_artists', 'f_genres', # bubbles
                'rec_tracks_names', 'rec_tracks_urls'
                'rec_artists_names', 'rec_artists_urls' # about
            ]

    # keys = variables, values = value for html page
    r = dict(zip(var_list, [None] * len(var_list))) 

    # splice pid from url
    pid1y, pid1x = pid1y[34 : -20], pid1x[34 : -20] 
    pid2 = pid2[34 : -20] 

    # create dataframes 
    df1y = create_df(pid1y, 1) # user1 likes
    df1x = create_df(pid1x, 0) # user1 dislikes
    df1 = combine_df([df1y, df1x]) # all user1
    df2 = create_df(pid2, 1) # user2

    user_data = get_data(uid, 'users')

    # artists, genres, features
    a1 = df1y['artist_ids'].tolist() # artists per person, w dupes (ids)
    a2 = df2['artist_ids'].tolist() 
    top_a1 = find_top(a1, 1) # user1's top 2 artists (ids)
    top_a2 = find_top(a2, 3) # user2's top 3 artists (ids)
    a = find_shared([a1, a2])[ : 5] # top 5 shared artists (ids)

    g1 = get_genres(a1)  # genres w/ dupes (strs)
    g2 = get_genres(a2)
    g = find_shared([g1, g2])[ : 5] # top 5 shared genres (strs)

    ###### PROFILE PAGE ######

    # HEADER
    # r['pfp'] = get_image(user_data)
    r['pfp'] = get_image(get_data(pid2, 'playlists'))
    r['name'] = user_data['display_name']
    r['compatibility'] = find_compatibility(df1[REDUCED_FEATURES], df1['likes'], df2[REDUCED_FEATURES], df2['likes']) * 100

    # PROMPTS 
    r['sim_features'] = str(find_features(df1y, df2, VERY_REDUCED_FEATURES))[1 : -1]

    # BUBBLES (shared + favs)
    r['s_artists'] = get_artist_info(a, 'name')
    r['s_genres'] = g
    r['f_artists'] = get_artist_info(top_a2, 'name')[ : 3]
    r['f_genres'] = [*set(g2)][ : 3]

    # ABOUT (RECS)
    # rec_tracks are jsons of data, not lists
    if len(a) != 0: # seed = shared artists
        rec_tracks = recommend_tracks(a, 'artists')
        r['rec_artists_names'] = recommend_artists(a, 0)
        r['rec_artists_urls'] = recommend_artists(a, 1)
    else: # no shared artists
        temp = [top_a1[0], top_a2[0], top_a2[1]] # top 2 artists per person
        r['rec_artists_names'] = recommend_artists(temp, 0)
        r['rec_artists_urls'] = recommend_artists(temp, 1)
        if len(g) != 0: # seed = shared genres
            rec_tracks = recommend_tracks(g, 'genres')
        else: # seed = top 2 artists per person
            rec_tracks = recommend_tracks(temp, 'artists')

    r['rec_tracks_names'] = recommend_track_names(rec_tracks)
    r['rec_tracks_urls'] = recommend_track_urls(rec_tracks)

    return r





