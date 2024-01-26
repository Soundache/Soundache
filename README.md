# <img src="static/favicon.ico" height=50> <a href="soundache.pythonanywhere.com">Soundache</a>
<img src="static/favicon.ico" height=20> <a href="soundache.pythonanywhere.com">Soundache</a> is a ~~Spotify ripoff~~ website where you can upload and listen to songs, as part of a high school group project.

The point of <img src="static/favicon.ico" height=20> <a href="soundache.pythonanywhere.com">Soundache</a> is to bring the decentralized philosophy of the Internet back to mediums like songs.  It's intended to be more of a song browser and search engine than a platform for uploading songs like Spotify or SoundCloud.  

Each time you open the link to a song, the frontend fetches the thumbnail and audio file from the server where the song is hosted. You can also host it at <img src="static/favicon.ico" height=20> <a href="soundache.pythonanywhere.com">Soundache</a>'s own songserver, running at a subdomain <a href="soundache.pythonanywhere.com/songserver">soundache.pythonanywhere.com/songserver</a>, but it doesn't treat this server any differently than it would a third party server.

The source code at `songserver.py` specifies the protocol that must be followed by third part servers hosting songs for Soundache.

_Written in Python + Flask and vanilla HTML/CSS/JS, with an SQLite database._

## API Examples
_(examples given in <a href="https://www.nushell.sh/">Nushell</a>)_

Soundache's API endpoints are the same as its subpages, except you use POST to get a response in JSON instead of HTML (even if you're not uploading any data to the server).

![Alt text](api_examples/Subpage%20user.png)

To login, use this and copy the session header to put in your successive requests
![Alt text](api_examples/Subpage%20login.png)

![Alt text](api_examples/Subpage%20likes.png)

## Credits
All the music currently at <a href="soundache.pythonanywhere.com">soundache.pythonanywhere.com</a> are royalty free and taken from Pixabay. Link to the original version is given in the playback page for each.

Special thanks to _us_, of course.

## To run the server yourself

Clone this repository and
```cmd
pip install -r requirements.txt
python main.py
```
(requires Python obviously)