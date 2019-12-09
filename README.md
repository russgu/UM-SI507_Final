## SI507 Final Project


#### Description:

This project aims to explore the Deezer API and provides an interface that can let user query most popular songs and artists, find
music videos and an artist's tweets, etc. 

It should: 
1) Utilize the concept of web api with/without api key/oauth token for authentication and caching the results.
2) Utilize of sqlite db to store basic informations about artists, tracks, and albums. 
3) Perform basic data processing such as number of tracks by genre, number of albums by artists, etc. 
4) Provide some visualization of popularity with plotly.
5) Unit testing on steps 1-3


#### Data Sources: 

1) Deezer API. Deezer API provides a lot of endpoints with different object models including artists, album, track, etc. which we can individually query and store. 
For basic information about the API please visit: https://developers.deezer.com/api for basic documentation

2) IMVDb API. In addition, the application would also search for the url of the corresponding music video through IMVDb API. 
For more details please visit: https://imvdb.com/developers/api/searching

3) Twitter API. The application would search tweets upon user input of an artist and find the keywords in the celebrities tweet. 
For more details please visit: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline

Data are gathered into sqlite db.

#### Presentation:

Using plotly to show Bar charts with popularity of tracks, # of followers of artists, etc. 

#### Files:

- Run the Final_Project.py on command line for interactive search. To run unit test file, run Final_Project_test.py.
- Json files are cached files generated from api calls so that the same request wouldn't need to go through the api twice.
- requirement.txt has all the needed libraries to run the program
- final.db is the sqlite database file that contains all the data requested.

#### Code Structure:

1. Class objects creates track, artist, album objects with data obtained from sqlite. They are used to show list of options when user enter commands for seeing videos or tweets.
2. Cache functions are for creating cache files after api calls.
3. Create tables generate tables: track, artist and album in sqlite db.
4. get_playlist grabs 100 tracks from a Deezer playlist "Global Top 100 songs". The program then iterate through the 100 tracks and get detailed information about tracks, artist and album through functions: get_track, get_artist,get_album. All the data are saved in sqlite db.
5. artist_followers, artist_album, track_popularity, album_genre does some sorting and aggregation on the obtained data and provides source for the visualization afterwards. Functions that start with "graph" are all the associated graphing utilities.
6. music_list list out top x tracks with highest likes and get_video selects one music from this list and direct user to the music video website.
7. artist_list does similar job to music_list but for artists and grab_twitter selects on artist and returns some keywords in the artist's twitter account.



