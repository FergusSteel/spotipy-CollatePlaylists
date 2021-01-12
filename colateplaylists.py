# Import Libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from pprint import pprint
import math

# Authorization FLow
scope = "playlist-modify-public user-library-read playlist-read-collaborative playlist-read-private"
user = "implementthislater"#input("insert Spotify UserID") #Place UserID here ,
token = util.prompt_for_user_token(user,scope,client_id="66cffc2706ab4a6fad63ece54c37e7ab",client_secret="fixthislater",redirect_uri='fixthislater')
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
    print(playlist_id)
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
def populate_playlist(playlists, playlistID):
    total = 0
    fulltracklist = []
    while total < 184:
        for playlist in playlists:
            x = playlist
            tracks = get_playlist_trackIDS(x)
            fulltracklist.extend(tracks)
            # Deleted Track
            if tracks == None:
                continue
            # Plalylists with 100 or less songs
            elif len(tracks) <= 100:
                sp.user_playlist_add_tracks(user, playlistID, tracks)
            # Longer Playlists
            else:
                tracklists = []
                for iteration in range(math.floor(len(tracks)/100)):
                    tracklists.append(tracks[100*iteration:(100*iteration)+100])
                tracklists.append(tracks[100*len(tracklists):])
                for list in tracklists:
                    if len(list) > 0:
                        sp.user_playlist_add_tracks(user, playlistID, list)
            total += 1
        return fulltracklist

def remove_duplicates(playlistID, tracks):
    #get list of duplicate songs
    #remove all occ. of found songs
    #re-add songs
    return

# Call
def main(userID=user, removeDuplicates=True):
    playlists = getPlaylistIDS(userID)
    x = sp.user_playlist_create(userID, name="BIG PLAYLIST ITS SO BIG", description="For Shuffling")
    tracklist = populate_playlist(playlists, x["id"])

main()
