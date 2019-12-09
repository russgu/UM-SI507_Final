## Final_Project_Spotify.py
## SI507 Final Project
## See project proposal file for an idea of the project

from secret import *
import sqlite3
import requests
import json
from requests_oauthlib import OAuth1
import plotly
import plotly.graph_objs as go
import webbrowser
import nltk 
from nltk.corpus import stopwords
import re
from collections import Counter

#### Requirements #####

# 1. Data should be acquired from API, get cached, and then writes into database
# 2. For each data source, need to capture at least 100 records. Each record has to have
# at least 5 fields associated with it.
# 3. Database has to have at least two tables 
# 4. Data Processing (aggregation,sort) code should draw data from database
# 5. Unit tests should show the data access, storage and processing are working correctly. At least
# three test cases and use at least 15 assertions


##### Define classes ####
class Artist():
#Attribute: spotify id,name,popularity,followers,genres
	def __init__(self,name,followers,link=None,nb_album=None,radio=None):
		self.name = name
		self.link = link
		self.num_album = nb_album
		self.followers = followers
		self.radio = radio

	def __str__(self):

		return self.name


class Album():
#Attribute: spotify_id,name,album type,artists,genres,release_date
	def __init__(self,name,duration,artist,genres,release_date):
		self.name = name
		self.duration = duration
		self.artist = artist
		self.genres = genres
		self.release_date = release_date

	def __str__(self):
		album = "{} released on {}".format(self.name,self.release_date)
		return album


class Track():
#Attribute: spotify id,name,album,artists,duration_ms,popularity
	def __init__(self,name,album,artists,duration,rank):
		self.name = name
		self.album = album
		self.artists = artists
		self.duration = duration
		self.rank = rank

	def __str__(self):
		track = "{} by {}".format(self.name,self.artists)
		return track



## Define caching function:
def get_unique_key(url,params={}):
	return url.split("/")[-1]

def cache_implementation(CACHE_FNAME,url,params = {}):

	uniq_id = get_unique_key(url,params)

	result = []

	try:
		with open(CACHE_FNAME) as json_file:
			CACHE_DICTION = json.load(json_file)
	except:
		CACHE_DICTION = {}

	## first, look in the cache to see if we already have this data

	if uniq_id in CACHE_DICTION:
		print("Getting cached data...")
		return CACHE_DICTION[uniq_id]
	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		resp = requests.get(url,params = params)
		CACHE_DICTION[uniq_id] = json.loads(resp.text)
		dumped_json_cache = json.dumps(CACHE_DICTION,indent = 4)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[uniq_id]


#### Create DB and Tables ####
DBNAME = 'final.db'

def create_tables():

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	cur.execute('CREATE TABLE "Artists" (\
		"Id"    INTEGER PRIMARY KEY AUTOINCREMENT,\
    	"name"    TEXT,\
	    "nb_album"  INTEGER,\
	    "radio"   BOOLEAN,\
	    "link"  TEXT,\
	    "followers" INTEGER \
	);')

	cur.execute('CREATE TABLE "Albums" ( \
	    "Id"  INTEGER PRIMARY KEY AUTOINCREMENT,\
	    "name"   TEXT,\
	    "duration"   REAL,\
	    "artist_Id"  INTEGER,\
	    "genres"   TEXT,\
	    "release_date"   DATE,\
	    FOREIGN KEY("artist_Id") REFERENCES "Artists"("Id")\
	);')

	cur.execute('CREATE TABLE "Tracks" ( \
	    "Id"  INTEGER PRIMARY KEY AUTOINCREMENT,\
	    "name"   TEXT,\
	    "album_Id"  INTEGER,\
	    "artist_Id"  INTEGER,\
	    "duration"  REAL,\
	    "rank" INTEGER,\
	    FOREIGN KEY("album_Id") REFERENCES "Albums"("Id"),\
	    FOREIGN KEY("artist_Id") REFERENCES "Artists"("Id")\
	);')

	conn.commit()
	conn.close()

#### API call and create objects ####

#get 100 tracks from global top 100 playlist. 
def get_playlist():

	playlist_url = "https://api.deezer.com/playlist/5501801362"
	CACHE_FNAME = "playlist.json"
	playlist = cache_implementation(CACHE_FNAME,playlist_url)

	return playlist

#get each of the track from 100 top playlist
def get_tracks():

	playlist = get_playlist()
	track_ids = [i["id"] for i in playlist["tracks"]["data"]]
	track_ids = list(set(track_ids))
	CACHE_FNAME = "tracks.json"
	tracks_url = "https://api.deezer.com/track/"

	for i in track_ids:
		track_json = cache_implementation(CACHE_FNAME,tracks_url+str(i))
		name = track_json["title"]
		album = track_json["album"]["title"]
		artists = track_json["artist"]["name"]
		duration = track_json["duration"]
		rank = track_json["rank"]

		statement = 'select Albums.Id from Albums where Albums.name = "{}" '
		query1 = statement.format(album)
		cur.execute(query1)
		albumid = cur.fetchone()
		albumid = albumid[0] if albumid != None else None

		statement2 = 'select Artists.Id from Artists where Artists.name = "{}" '
		query2 = statement2.format(artists)
		cur.execute(query2)
		artistid = cur.fetchone()
		artistid = artistid[0] if artistid != None else None

		statement_tracks = 'INSERT INTO Tracks VALUES (?,?,?,?,?,?)'
		insertion = (None,name,albumid,artistid,duration,rank)

		cur.execute(statement_tracks,insertion)


#get artists from above result in tracks
def get_artists():

	playlist = get_playlist()
	artist_ids = [i["artist"]["id"] for i in playlist["tracks"]["data"]]
	artist_ids = list(set(artist_ids))
	CACHE_FNAME = "artists.json"
	artist_url = "https://api.deezer.com/artist/"

	for i in artist_ids:
		artist_json = cache_implementation(CACHE_FNAME,artist_url+str(i))
		link = artist_json["link"]
		nb_album = artist_json["nb_album"]
		radio = artist_json["radio"]
		name = artist_json["name"]
		followers = artist_json["nb_fan"]
		#Insert record into DB
		statement_artist = 'INSERT INTO Artists VALUES (?,?,?,?,?,?)'
		insertion = (None,name,nb_album,radio,link,followers)

		cur.execute(statement_artist,insertion)

#get albums from above result in tracks. 
def get_album():

	playlist = get_playlist()
	album_ids = [i["album"]["id"] for i in playlist["tracks"]["data"]]
	album_ids = list(set(album_ids))
	CACHE_FNAME = "album.json"
	album_url = "https://api.deezer.com/album/"

	for i in album_ids:
		album_json = cache_implementation(CACHE_FNAME,album_url+str(i))
		if "error" in album_json:
			continue
		name = album_json["title"]
		duration = album_json["duration"]
		artist = album_json["artist"]["name"]
		genres = (album_json["genres"]["data"][0]["name"] if album_json["genres"]["data"] else None)
		release_date = album_json["release_date"]
		#Insert record into DB
		statement = 'select Artists.Id from Artists where Artists.name = "{}" '
		query1 = statement.format(artist)
		cur.execute(query1)
		artistid = cur.fetchone()
		artistid = artistid[0] if artistid != None else None

		statement_album = 'INSERT INTO Albums VALUES (?,?,?,?,?,?)'
		insertion = (None,name,duration,artistid,genres,release_date)

		cur.execute(statement_album,insertion)

# Uncomment these function calls the first time you run this program
#create_tables()
#get_playlist()
#get_tracks()
#get_artists()
#get_album()

#### Data Processing, Retrieving from DB and display ####

# Grab top popular artists input by user. Default is 10.

def artist_followers(num_artist=10):

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select Id, name, followers from Artists order by followers desc limit " + str(num_artist)

	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	return output


# Grab most prolific artists input by user.
def artist_album(num_artist=10):

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select Id, name, nb_album from Artists order by nb_album desc limit " + str(num_artist)

	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	return output


# Grab the popularity of the top tracks input by user. Default is 10
def track_popularity(num_track=10):

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select t.Id, t.name, a.name as artist, al.name as album, t.rank as num_likes,t.duration from Tracks t\
	left join Artists a\
	on a.Id = t.artist_Id\
	left join Albums al\
	on al.Id = t.album_Id\
	order by t.rank desc limit " + str(num_track)

	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	return output


# Grab number of albums by genre
def albums_genre():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select genres,count(Id) from Albums group by genres order by count(Id) desc"
	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	return output


#### Graphing ####

# Graph top artist followers
def graph_followers(query_result):

	fig = go.Figure(go.Bar(

		x=[q[2] for q in query_result],
		y=[q[1] for q in query_result],
		orientation='h'
		))

	fig.update_layout(
    title="followers by artist",
    xaxis_title="#Followers",
    yaxis_title="Artist",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

	fig.show()


# Graph top prolific artist 
def graph_artist_album(query_result):
	
	fig = go.Figure(go.Bar(

		x=[q[2] for q in query_result],
		y=[q[1] for q in query_result],
		orientation='h'))

	fig.update_layout(
    title="#Albums by artist",
    xaxis_title="#Albums",
    yaxis_title="Artist",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

	fig.show()


# Graph top track popularity
def graph_track_popularity(query_result):
	
	fig = go.Figure(go.Bar(

		x=[q[4] for q in query_result],
		y=[q[1] for q in query_result],
		orientation='h'))

	fig.update_layout(
    title="#likes by track",
    xaxis_title="#likes",
    yaxis_title="Track",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

	fig.show()


# Graph number of albums by genre
def graph_genre(query_result):
	
	fig = go.Figure(go.Bar(

		x=[q[1] for q in query_result],
		y=[q[0] for q in query_result],
		orientation='h'))

	fig.update_layout(
    title="#albums by genre",
    xaxis_title="#albums",
    yaxis_title="Genre",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ))

	fig.show()


#### List musics ####
def music_list(num_music=20):
	# num_music can range from 1 - 100

	songs = []

	if num_music > 100:
		print("music selection out of range.")
		return

	tracks = track_popularity(num_music)
	for t in tracks:
		#name,album,artists,duration,rank
		songs.append(t[0])
		track_obj = Track(name = t[1],artists = t[2],album = t[3],duration = t[5],rank = t[4])
		string = "{}. {}".format(t[0],track_obj.__str__())
		print(string)

	return songs


#### Get music video from imvdb ####

def get_video(track_id):

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select t.name, a.name as artist from Tracks t\
	left join Artists a\
	on a.Id = t.artist_Id where t.Id = {}".format(track_id)

	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	track = output[0][0]
	artist = output[0][1]

	video_url = "https://imvdb.com/api/v1/search/videos"
	params = {}
	params["q"] = artist.strip().replace(" ","+") +" + "+track.strip().replace(" ","+")

	response = requests.get(video_url,params)
	video_json = json.loads(response.text)

	url = video_json["results"][0]["url"]
	print("Launching" + url + " in web browser...")
	webbrowser.open(url)


#### Grab artist twitter ####

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_key, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

def artist_list(num_artist=20):

	artists = []

	results = artist_followers(num_artist)
	for r in results:
		#name,album,artists,duration,rank
		artists.append(r[0])
		artist_obj = Artist(name = r[1],followers = r[2])
		string = "{}. {}".format(r[0],artist_obj.__str__())
		print(string)

	return artists


def grab_twitter(artist_id,num_tweets=20,k=5):

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()

	query = "select Id, name from Artists where Id = {}".format(artist_id)

	output = cur.execute(query).fetchall()

	conn.commit()
	conn.close()

	artist = output[0][1]

	base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

	pd = {}
	pd["screen_name"] = artist.lower().replace(" ","")
	pd["count"] = num_tweets

	json_string = requests.get(base_url, params = pd, auth = auth)
	results = json.loads(json_string.text)

	#get text and clean text
	if "errors" not in results:
		texts = [i['text'] for i in results]
		texts = ' '.join(texts)
		texts = re.sub("[^a-zA-Z ]","",texts) #remove characters that is not an alphabetic or space
		texts = re.sub("https([a-zA-Z])+|RT|http([a-zA-Z])+","",texts) #ignore words starting with 'http', 'https', and 'RT	  
		texts = texts.lower() #convert

		#tokenize and remove stop words
		stops = set(stopwords.words("english"))
		tokens = nltk.word_tokenize(texts)
		tokens = [t for t in tokens if t not in stops]

	else:
		tokens = "Page not exist"

	print(tokens)


#### Help page ####
def load_help_text():
	with open('help.txt') as f:
		return f.read()


#### Interactive Search ####

def interactive_search():

	user_input = input("Enter command(or 'help' for options):")
	user_input = user_input.split(" ")

	if user_input[0] == "help":
		print(load_help_text())
		interactive_search()

	elif user_input[0] == "exit":
		print("bye")
		exit()

	elif user_input[0] in ["graph_followers","graph_albums","graph_tracks","video","twitter","graph_genre"]:

		command = user_input[0]

		if len(user_input)==2:
			if user_input[1].isdigit():
				parameter = int(user_input[1])

			else:
				print("Wrong input. Second argument should be an integer and without extra spaces.")
				interactive_search()

		if len(user_input)>2:
			print("Wrong input.Too many arguments.")
			interactive_search()

		if command =="graph_followers":
			data = (artist_followers(parameter) if len(user_input)==2 else artist_followers())
			graph_followers(data)

		if command == "graph_albums":
			data = (artist_album(parameter) if len(user_input)==2 else artist_album())
			graph_artist_album(data)

		if command == "graph_tracks":
			data = (track_popularity(parameter) if len(user_input)==2 else track_popularity())
			graph_track_popularity(data)

		if command == "graph_genre":
			data = albums_genre()
			graph_genre(data)

		if command == "video":
			tracks = (music_list(parameter) if len(user_input)==2 else music_list())
			select = input("select a song by index: ")

			while not select.isdigit() or (int(select) not in tracks):
				print("Wrong input. Index should be an integer or index not in above list.")
				select = input("select a song by index: ")

			get_video(int(select))

		if command == "twitter":
			artists = (artist_list(parameter) if len(user_input)==2 else artist_list())
			select = input("select an artist by index: ")

			while not select.isdigit() or (int(select) not in artists):
				print("Wrong input. Index should be an integer or index not in above list.")
				select = input("select an artist by index: ")

			grab_twitter(int(select))

		interactive_search()


	else:
		print("Wrong input. Please see 'help' for available commands: ")
		interactive_search()


if __name__ == "__main__":
    interactive_search()
    pass
