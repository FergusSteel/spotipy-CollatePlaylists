# Import Libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from pprint import pprint
import math

# Authorization FLow
scope = "playlist-modify-public user-library-read playlist-read-collaborative playlist-read-private"
user = ""#input("insert Spotify UserID") #Place UserID here ,
token = util.prompt_for_user_token(user,scope,client_id="66cffc2706ab4a6fad63ece54c37e7ab",client_secret="idkhow secret this is meant to be",redirect_uri='http://localhost:8080')
sp = spotipy.Spotify(auth=token)


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
                if curtrack["id"] != None and curtrack["track"]:
                    trackIDS.append(curtrack["id"])
            if tracks['next'] != None:
                tracks = sp.next(tracks)
            else:
                tracks = None
        return trackIDS

# Function to add tracks to playlist from list of playlists
#I think i just redo this function, use .extend on calling get_playlist_trackIDS() and then iterate over that using the math.floor(x/100) or whatever it is
# if duplicates are on then do it normally if they are off simply make the list a set then do it.
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

# Call
def main(userID=user, removeDuplicates=True):
    playlists = getPlaylistIDS(userID)
    x = sp.user_playlist_create(userID, name="BIG PLAYLIST ITS SO BIG", description="its so big")
    tracklist = get_tracklist(playlists)
    if removeDuplicates:
        tracklist = set(tracklist)
        tracklist = list(tracklist)
    #add tracks
    for cent_tracks in range(math.floor(len(tracklist)/100)):
        sp.user_playlist_add_tracks(user, x["id"], tracklist[100*cent_tracks:(100*cent_tracks)+100])
    sp.user_playlist_add_tracks(user, x["id"], tracklist[math.floor(len(tracklist)/100)*100:])

main()
