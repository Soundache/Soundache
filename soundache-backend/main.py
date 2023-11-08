from flask import Flask, render_template, request, abort, jsonify, session, url_for, send_from_directory, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, LargeBinary, BINARY
import difflib
import metrohash

SOUNDACHE = "Soundache"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)

HASH_STR_64 = lambda s: metrohash.hash64_int(s, seed=0) // 2

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer)
    # thumbnail: Mapped = mapped_column(LargeBinary, nullable=True)
    # midi = mapped_column(LargeBinary)
    # lyrics = mapped_column(LargeBinary)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    passwordHash: Mapped[str] = mapped_column(String, nullable=False)
    taste: Mapped[str] = mapped_column(String)

@app.route("/")
def main_page():
    # db.session.add(User(id=HASH_STR_64('ADMIN'), email='ADMIN', passwordHash=generate_password_hash('vvsafepswd'), taste=''))
    # db.session.commit()
    # print(db.session.execute(db.select(User.passwordHash)).scalar_one_or_none())
    return render_template("index.html", songs=[])

@app.route("/search")
def search():
    query = request.args.get("searchbar")
    is_API_call = request.headers.get("API", default=False)
    if query is None:
        if not is_API_call:
            return render_template("search.html", string="Start typing yo")
        else:
            return jsonify(error="No search query provided"), 400
    elements = ['Actinium', 'Aluminum', 'Americium', 'Antimony', 'Argon', 'Arsenic', 'Astatine', 'Barium', 'Berkelium', 'Beryllium', 'Bismuth', 'Bohrium', 'Boron', 'Bromine', 'Cadmium', 'Calcium', 'Californium', 'Carbon', 'Cerium', 'Cesium', 'Chlorine', 'Chromium', 'Cobalt', 'Copper', 'Curium', 'Darmstadtium', 'Dubnium', 'Dysprosium', 'Einsteinium', 'Erbium', 'Europium', 'Fermium', 'Fluorine', 'Francium', 'Gadolinium', 'Gallium', 'Germanium', 'Gold', 'Hafnium', 'Hassium', 'Helium', 'Holmium', 'Hydrogen','Indium','Iodine','Iridium','Iron','Krypton','Lanthanum','Lawrencium','Lead','Lithium','Livermorium','Lutetium','Magnesium','Manganese','Meitnerium','Mendelevium','Mercury','Molybdenum','Moscovium','Neodymium','Neon','Neptunium','Nickel','Nihonium','Niobium','Nitrogen','Nobelium','Oganesson','Osmium','Oxygen','Palladium','Phosphorus','Platinum','Plutonium','Polonium','Potassium','Praseodymium','Promethium','Protactinium','Radium','Radon','Rhenium', 'Rhodium'
                ]
    lst = difflib.get_close_matches(query.capitalize(), elements, 16, min(0.8, 0.1*len(query)))

    if is_API_call:
        return {"results": lst}
    return render_template("search.html", string=f"You searched {query}<br/>{lst}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        pwd_hash = db.session.execute(
            db.select(User.passwordHash).where(User.id == HASH_STR_64(request.form['email']))
        ).scalar_one_or_none()
        if pwd_hash is None:
            return jsonify(error="No such email-ID has been registered", email=request.form['email']), 403
        else:
            if check_password_hash(pwd_hash, request.form["password"]):
                return jsonify(), 200
            else:
                return jsonify(error="Wrong password"), 403
    return jsonify(error="This endpoint only supports GET and POST"), 400
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        user_exists = db.session.execute(
            db.select(User.email).where(User.id == HASH_STR_64(request.form['email']))
        ).scalar_one_or_none()
        if user_exists:
            return jsonify(error="User already exists"), 409
        new_user = User(id=HASH_STR_64(request.form['email']),
                        email=request.form['email'],
                        passwordHash=generate_password_hash(request.form['password']),
                        taste="")
        db.session.add(new_user)
        db.session.commit()
        return jsonify(), 200
    return jsonify(error="This endpoint only supports GET and POST"), 400

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
