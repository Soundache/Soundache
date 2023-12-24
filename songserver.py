from flask import Flask, request, make_response, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, LargeBinary, BINARY
import metrohash
import toml

NAME = "Soundache Song Database"
SECRETS = toml.load('instance/secrets.toml')
HASH_STR_64 = lambda s: metrohash.hash64_int(s, seed=0) // 2

app = Flask(NAME)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
app.secret_key = SECRETS['secret_key']   # secrets.token_hex()
db = SQLAlchemy()
db.init_app(app)

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer)
    # artistName: Mapped[str] = mapped_column(String)
    thumbnail: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    songFile: Mapped[bytes] = mapped_column(LargeBinary)
    # midi = mapped_column(LargeBinary)
    # lyrics = mapped_column(LargeBinary)

@app.route("/")
def index():
    songID = request.query.get('id')
    file = db.session.execute(db.select(Song.songFile, Song.thumbnail).where(Song.id==songID)).scalar_one_or_none()
    if file is None:
        return jsonify(error="Song not found!"), 404
    return send_file(file), 200

@app.route("/upload", methods=['GET', 'POST', 'OPTIONS'])
def upload():
    if request.method != 'POST':
        return {}, 200
    try:
        artistId = HASH_STR_64(request.form['email'])
        songName = request.form['name']
        id = HASH_STR_64(songName)
        song = Song(name=songName, id=id, artistId=artistId, thumbnail=request.form['thumbnail-file'], 
                    songFile=request.form['song-file'])
    except KeyError:
        return jsonify(error="Expected a form with 'email', 'name', 'thumbnail-file' and 'song-file' entries"), 403
    # TODO: check if song of same name exists alr
    db.session.add(song)
    db.session.commit()
    return {}, 200

@app.route("/thumbnail", methods=['GET'])
def thumbnail():
    songID = request.query.get('id')
    file = db.session.execute(db.select(Song.thumbnail).where(Song.id==songID)).scalar_one_or_none()
    if file is None:
        return jsonify(error="Song not found!"), 404
    return send_file(file), 200

@app.route("/music", methods=['GET'])
def music():
    songID = request.query.get('id')
    file = db.session.execute(db.select(Song.songFile).where(Song.id==songID)).scalar_one_or_none()
    if file is None:
        return jsonify(error="Song not found!"), 404
    return send_file(file), 200

@app.after_request
def add_header(response):  # To avoid CORS exceptions in the frontend
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)