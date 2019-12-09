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
