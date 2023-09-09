from flask import Flask, render_template, request, session, url_for, send_from_directory, send_file
import sqlite3
import difflib

SOUNDACHE = "Soundache"

app = Flask(__name__)

@app.route("/")
def main_page():
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()
    fetched = cursor.execute("SELECT * FROM recommended_songs")
    return render_template("index.html", songs=fetched.fetchall())

@app.route("/search")
def search():
    query = request.args.get("searchbar")
    elements = ['Actinium', 'Aluminum', 'Americium', 'Antimony', 'Argon', 'Arsenic', 'Astatine', 'Barium', 'Berkelium', 'Beryllium', 'Bismuth', 'Bohrium', 'Boron', 'Bromine', 'Cadmium', 'Calcium', 'Californium', 'Carbon', 'Cerium', 'Cesium', 'Chlorine', 'Chromium', 'Cobalt', 'Copper', 'Curium', 'Darmstadtium', 'Dubnium', 'Dysprosium', 'Einsteinium', 'Erbium', 'Europium', 'Fermium', 'Fluorine', 'Francium', 'Gadolinium', 'Gallium', 'Germanium', 'Gold', 'Hafnium', 'Hassium', 'Helium', 'Holmium', 'Hydrogen','Indium','Iodine','Iridium','Iron','Krypton','Lanthanum','Lawrencium','Lead','Lithium','Livermorium','Lutetium','Magnesium','Manganese','Meitnerium','Mendelevium','Mercury','Molybdenum','Moscovium','Neodymium','Neon','Neptunium','Nickel','Nihonium','Niobium','Nitrogen','Nobelium','Oganesson','Osmium','Oxygen','Palladium','Phosphorus','Platinum','Plutonium','Polonium','Potassium','Praseodymium','Promethium','Protactinium','Radium','Radon','Rhenium', 'Rhodium'
                ]
    lst = difflib.get_close_matches(query.capitalize(), elements, 16, min(0.8, 0.1*len(query)))

    if request.headers.get("API", False):
        return {"results": lst}
    return f"You searched {query}\n{lst}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:  # request.method = POST
        print(request.form["email"], request.form["password"])
        return "BOO"
