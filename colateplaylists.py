# Import Libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from pprint import pprint
import math
import cgitb
import sys

# Function to create list of playlist ids
def getPlaylistIDS(userID):
    playlists = sp.user_playlists(userID)
    playlistIDS = []
    while playlists:
        for playlist in playlists['items']:
            playlistIDS.append(playlist["id"])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return playlistIDS


#Function to create list of track IDS from Playlist ID
def get_playlist_trackIDS(playlist_id):
    trackIDS = []
    tracks = sp.playlist_tracks(playlist_id)
    if tracks["items"] != []:
        while tracks:
            for track in tracks['items']:
                curtrack = track["track"]
                try:
                    if curtrack["id"] != None and curtrack["track"]:
                        trackIDS.append(curtrack["id"])
                except:
                    pass
            if tracks['next'] != None:
                tracks = sp.next(tracks)
            else:
                tracks = None
        return trackIDS

# Function to add tracks to playlist from list of playlists
def get_tracklist(playlists):
    total = 0
    fulltracklist = []
    for playlist in playlists:
        tracks = get_playlist_trackIDS(playlist)
            # Deleted Track
        if tracks == None:
            continue
            # Plalylists with 100 or less songs
        else:
            fulltracklist.extend(tracks)
    return fulltracklist

#Add functionality to add liked songs to the playlist aswell :)
def get_saved_songs(user):
    tracks = sp.current_user_saved_tracks()
    likedsongs = []
    if tracks["items"] != []:
        while tracks:
            for track in tracks["items"]:
                curtrack = track["track"]
                if curtrack["id"] != None and curtrack["type"] == "track":
                    likedsongs.append(curtrack["id"])
            if tracks['next'] != None:
                tracks = sp.next(tracks)
            else:
                tracks = None
    return likedsongs

def colate(sp, userID, pn, removeDuplicates=True, addSavedSongs=True):
    playlists = getPlaylistIDS(userID)
    x = sp.user_playlist_create(userID, name=pn, description="")
    tracklist = get_tracklist(playlists)
    if addSavedSongs:
        tracklist.extend(get_saved_songs(userID))
    if removeDuplicates:
        tracklist = set(tracklist)
        tracklist = list(tracklist)
    #add tracks
    for cent_tracks in range(math.floor(len(tracklist)/100)):
        sp.user_playlist_add_tracks(user, x["id"], tracklist[100*cent_tracks:(100*cent_tracks)+100])
    sp.user_playlist_add_tracks(user, x["id"], tracklist[math.floor(len(tracklist)/100)*100:])

if __name__ == "__main__":
    # Authorization FLow
    scope = "playlist-modify-public user-library-read playlist-read-collaborative playlist-read-private"
    user = input("insert Spotify UserID\n") #Place UserID here ,
    print()
    playlist_name = input("Insert Playlist Name:\n")
    print()


    token = util.prompt_for_user_token(user,scope,client_id="66cffc2706ab4a6fad63ece54c37e7ab",client_secret="b7764586c9084402b423c49f6ebe1c5c",redirect_uri='127.0.0.1:9090')
    sp = spotipy.Spotify(auth=token)

    colate(sp, user, pn)
