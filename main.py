from flask import Flask, render_template, request, abort, jsonify, session, make_response, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from typing import Set, List
from sqlalchemy import Integer, String, LargeBinary, BINARY, JSON, ForeignKey
import difflib
import metrohash
import secrets
import toml

SOUNDACHE = "Soundache"
SECRETS = toml.load('instance/secrets.toml')

app = Flask(SOUNDACHE)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = SECRETS['secret_key']   # secrets.token_hex()
db = SQLAlchemy()
db.init_app(app)

HASH_STR_64 = lambda s: metrohash.hash64_int(s, seed=0) // 2

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    passwordHash: Mapped[str] = mapped_column(String, nullable=False)
    # likes: Mapped[List["Music"]] = mapped_column(Integer)
    # channel: Mapped[List["Music"]] = mapped_column(Integer)
    # channel = relationship()

class Music(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistId: Mapped[int] = mapped_column(ForeignKey(User.id), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    # dislikes: Mapped[int] = mapped_column(Integer, default=0)
    # thumnail: Mapped[bytes] = mapped_column(BINARY)
    derivativeOf: Mapped[str] = mapped_column(String, nullable=True)

class Keywords(db.Model):
    keyword: Mapped[str] = mapped_column(String, primary_key=True)
    # songs: Mapped[Set[Music]] = mapped_column(Set, nullable=False)

@app.route("/")
def main_page():
    songs = db.session.execute(
        db.select(User.email, Music).where(User.id == Music.artistId).order_by(Music.views, Music.likes)
    ).fetchmany(50)
    return render_template("index.html", songs=songs)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        query = request.args.get("searchbar")
        if query is None or query == "":
            return jsonify(error="No search query provided"), 400
        elements = ['Actinium', 'Aluminum', 'Americium', 'Antimony', 'Argon', 'Arsenic', 'Astatine', 
                    'Barium', 'Berkelium', 'Beryllium', 'Bismuth', 'Bohrium', 'Boron', 'Bromine', 
                    'Cadmium', 'Calcium', 'Californium', 'Carbon', 'Cerium', 'Cesium', 'Chlorine', 'Chromium', 'Cobalt', 'Copper', 'Curium', 
                    'Darmstadtium', 'Dubnium', 'Dysprosium', 'Einsteinium', 'Erbium', 'Europium', 'Fermium', 'Fluorine', 'Francium', 
                    'Gadolinium', 'Gallium', 'Germanium', 'Gold', 'Hafnium', 'Hassium', 'Helium', 'Holmium', 'Hydrogen',
                    'Indium','Iodine','Iridium','Iron',
                    'Krypton','Lanthanum','Lawrencium','Lead','Lithium','Livermorium','Lutetium',
                    'Magnesium','Manganese','Meitnerium','Mendelevium','Mercury','Molybdenum','Moscovium',
                    'Neodymium','Neon','Neptunium','Nickel','Nihonium','Niobium','Nitrogen','Nobelium','Oganesson','Osmium','Oxygen',
                    'Palladium','Phosphorus','Platinum','Plutonium','Polonium','Potassium','Praseodymium','Promethium','Protactinium',
                    'Radium','Radon','Rhenium', 'Rhodium'
                    ]
        lst = difflib.get_close_matches(query.capitalize(), elements, 16, min(0.8, 0.1*len(query)))
        return jsonify(results=lst), 200
    return jsonify(error="This endpoint only supports GET and POST"), 405

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", session=session)
    elif request.method == "POST":
        if not request.form.get('email') or not request.form.get('password'):
            return jsonify(error="Expected form with 'email' and 'password' entries"), 422
        pwd_hash = db.session.execute(
            db.select(User.passwordHash).where(User.id == HASH_STR_64(request.form['email']))
        ).scalar_one_or_none()
        if pwd_hash is None:
            return jsonify(error="Either email or password is wrong"), 403
        else:
            if check_password_hash(pwd_hash, request.form["password"]):
                session['email'] = request.form["email"]
                return jsonify(), 200
            else:
                session.clear()
                return jsonify(error="Either email or password is wrong"), 403
    return jsonify(error="This endpoint only supports GET and POST"), 405
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", session=session)
    elif request.method == "POST":
        user_exists = db.session.execute(
            db.select(User.email).where(User.id == HASH_STR_64(request.form['email']))
        ).scalar_one_or_none()
        if user_exists:
            return jsonify(error="User already exists"), 409
        new_user = User(id=HASH_STR_64(request.form['email']),
                        email=request.form['email'],
                        passwordHash=generate_password_hash(request.form['password']))
        db.session.add(new_user)
        db.session.commit()
        session['email'] = request.form["email"]
        return jsonify(), 200
    return jsonify(error="This endpoint only supports GET and POST"), 405 

@app.route("/playback")
def playback():
    song_id = request.args.get('watch')
    print(song_id)
    return render_template("playback.html", thumbnail=None, audio=None)

@app.route("/likes")
def likes():
    pass

@app.route("/user", methods=['GET', 'POST'])
def user():
    userID = request.args.get('id') or request.args.get('name') or session.get('email')
    if not userID:
        if request.method == 'GET':
            return render_template("user.html", has_songs=True, artistName='')
        else:
            return jsonify(error="Must either be signed in or provide a query string!"), 403
        
    for char in userID:
        if char.isalpha():
            userID = HASH_STR_64(userID)
            break

    if isinstance(userID, str):
        userID = int(userID)

    username = db.session.execute(db.select(User.email).where(User.id == userID)).scalar_one_or_none()
    if username is None:
        if request.method == 'GET':
            return render_template("user.html", no_such_user=True)
        return jsonify(error="No such user exists!"), 404

    songs = db.session.execute(
        db.select(Music.id, Music.name, Music.link, Music.views, Music.likes).where(Music.artistId == userID)
    ).all()

    if request.method == 'GET':
        return render_template("user.html", songs=songs, has_no_songs=len(songs)==0, artistName=username.split('@')[0], 
                               no_such_user=False)
    songs_out = []
    for i in songs:
        songs_out.append({'id': i.id, 'name': i.name, 'link': i.link, 'views': i.views, 'likes': i.likes})
    return jsonify(username=username, userID=userID, songs=songs_out), 200

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/upload", methods=['GET', 'POST'])
def upload_songs():
    if request.method == 'GET':
        return render_template("upload-song.html", session=session)
    elif request.method == 'POST':
        if not session.get('email'):
            return jsonify(error="Need to be signed in to upload!"), 401
        artistId = HASH_STR_64(session['email'])
        songName = request.form['name']
        id = HASH_STR_64(songName)
        derivativeOf = request.form['derivativeOf']
        url = request.form['urlToWork'].removesuffix('/')
        if request.form['hostIsSoundache'] == 'true':
            url = ':8000/' + str(id)
        song_exists = db.session.execute(
            db.select(Music.id).where(Music.id == id and Music.artistId == artistId)
        ).scalar_one_or_none()
        if song_exists:
            return jsonify(error="Song of same name and from same user already exists!"), 409
        db.session.add(Music(id=id, name=songName, artistId=artistId, link=url, derivativeOf=derivativeOf))
        db.session.commit()
        return jsonify(), 200
    return jsonify(error="This endpoint only supports GET and POST"), 405

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
