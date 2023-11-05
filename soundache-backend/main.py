from flask import Flask, render_template, request, session, url_for, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import sqlite3
import difflib

SOUNDACHE = "Soundache"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer)

@app.route("/")
def main_page():
    # db_connection = sqlite3.connect("database.db")
    # cursor = db_connection.cursor()
    # fetched = cursor.execute("SELECT * FROM recommended_songs")
    return render_template("index.html", songs=[])

@app.route("/search")
def search():
    query = request.args.get("searchbar")
    is_API_call = request.headers.get("API", default=False)
    if query is None:
        if not is_API_call:
            return render_template("search.html", string="Start typing yo")
        else:
            return 
    elements = ['Actinium', 'Aluminum', 'Americium', 'Antimony', 'Argon', 'Arsenic', 'Astatine', 'Barium', 'Berkelium', 'Beryllium', 'Bismuth', 'Bohrium', 'Boron', 'Bromine', 'Cadmium', 'Calcium', 'Californium', 'Carbon', 'Cerium', 'Cesium', 'Chlorine', 'Chromium', 'Cobalt', 'Copper', 'Curium', 'Darmstadtium', 'Dubnium', 'Dysprosium', 'Einsteinium', 'Erbium', 'Europium', 'Fermium', 'Fluorine', 'Francium', 'Gadolinium', 'Gallium', 'Germanium', 'Gold', 'Hafnium', 'Hassium', 'Helium', 'Holmium', 'Hydrogen','Indium','Iodine','Iridium','Iron','Krypton','Lanthanum','Lawrencium','Lead','Lithium','Livermorium','Lutetium','Magnesium','Manganese','Meitnerium','Mendelevium','Mercury','Molybdenum','Moscovium','Neodymium','Neon','Neptunium','Nickel','Nihonium','Niobium','Nitrogen','Nobelium','Oganesson','Osmium','Oxygen','Palladium','Phosphorus','Platinum','Plutonium','Polonium','Potassium','Praseodymium','Promethium','Protactinium','Radium','Radon','Rhenium', 'Rhodium'
                ]
    lst = difflib.get_close_matches(query.capitalize(), elements, 16, min(0.8, 0.1*len(query)))

    if is_API_call:
        return {"results": lst}
    return render_template("search.html", string=f"You searched {query}\n{lst}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:  # request.method = POST
        print(request.form["email"], request.form["password"])
        return "BOO"


if __name__ == "__main__":
    app.run(debug=False, port=5000)
