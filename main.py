from pyyoutube import Api
import spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import json

def sync(sp_play_list_id,playlist_Id):
    load_dotenv()
    # load env
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    redirect_uri = os.getenv("redirect_uri") 
    scope = os.getenv("scope") 
    key = os.getenv("Api_key") 
    #sp_play_list_id = os.getenv("sp_play_list_id")


    # spotify auth manging
    auth_manager = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # youtube api managing
    api = Api(api_key=key)

    # get the titels from the youtube play list
    info = api.get_playlist_items(playlist_id=playlist_Id,count=100)
    items = {"songs":[]}

    for item in info.items:
        try:
            r = str(item.snippet.title)
            r = r.replace('\"',"")
            r = r.replace('(Official Video)',"")
            lim = r.find("|")
            items["songs"].append(r[0:lim])
        except:
            continue

    #get the id for the track from spotify 
    results = [] 
    for item in set(items["songs"]):
        artist,track = item.split("-")
        re = sp.search(q = 'artist:' + artist + ' track:' + track, type='track')
        try :
            track_id = re['tracks']['items'][0]['id']
            results.append('spotify:track:'+track_id)
        except:
            continue    

    # save to a play list in spotify 
    sp.playlist_add_items(playlist_id=sp_play_list_id,items=results)
    return 200