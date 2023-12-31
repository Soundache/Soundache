from flask import Flask, request, make_response, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, LargeBinary, BINARY
import metrohash
from io import BytesIO

NAME = "Soundache Song Database"
HASH_STR_64 = lambda s: metrohash.hash64_int(s, seed=0) // 2

app = Flask(NAME)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
db = SQLAlchemy()
db.init_app(app)

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistName: Mapped[str] = mapped_column(String)
    thumbnailFileType: Mapped[str] = mapped_column(String, nullable=False)
    songFileType: Mapped[str] = mapped_column(String, nullable=False)
    thumbnail: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    songFile: Mapped[bytes] = mapped_column(LargeBinary)
    # lyrics = mapped_column(LargeBinary)

@app.route("/", methods=['GET', 'POST', 'OPTIONS', 'HEAD', 'PUT'])
def index():
    return jsonify(
        error="API endpoints available are '/upload', '/<songID:integer>/thumbnail' and '/<songID:integer>/music'"
    ), 404

@app.route("/<songID>/thumbnail", methods=['GET'])
def thumbnail(songID):
    artistID, songID = songID.split('.')
    resource = db.session.execute(db.select(Song.thumbnailFileType, Song.thumbnail)\
                                  .where(Song.id==songID and Song.artistID == artistID)).all()
    if not resource:
        return jsonify(error="Song not found!"), 404
    return send_file(BytesIO(resource[0].thumbnail), download_name=f"thumbnail.{resource[0].thumbnailFileType}"), 200

@app.route("/<songID>/music", methods=['GET'])
def music(songID):
    artistID, songID = songID.split('.')
    resource = db.session.execute(db.select(Song.songFileType, Song.songFile)\
                                  .where(Song.id==songID and Song.artistID == artistID)).all()
    if not resource:
        return jsonify(error="Song not found!"), 404
    return send_file(BytesIO(resource[0].songFile), download_name=f"song.{resource[0].songFileType}"), 200

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method != 'POST':
        return jsonify(), 200
    
    try:
        artistName = request.form['email']
        artistId = HASH_STR_64(artistName)
        songName = request.form['name']
        id = HASH_STR_64(songName)
        thumbnailFileType = request.files['thumbnail-file'].filename.split('.')[-1]
        songFileType = request.files['song-file'].filename.split('.')[-1]
        thumbnail = request.files['thumbnail-file'].read()
        songFile = request.files['song-file'].read()
    except KeyError:
        return jsonify(error="Expected a form with 'email', 'name', 'thumbnail-file' and 'song-file' entries"), 422
    
    if db.session.execute(db.select(Song.id).where(Song.id == id and Song.artistID == artistId)).scalar_one_or_none():
        return jsonify(error="Song of same name and from the same artist already exists!"), 409

    song = Song(name=songName, id=id, artistID=artistId, thumbnail=thumbnail, artistName=artistName,
                songFile=songFile, thumbnailFileType=thumbnailFileType, songFileType=songFileType)
    db.session.add(song)
    db.session.commit()
    return {}, 200

@app.after_request
def add_header(response):  # To avoid CORS exceptions in the frontend
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)