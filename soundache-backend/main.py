from flask import Flask, render_template, request, session, url_for, send_from_directory, send_file
import sqlite3

SOUNDACHE = "Soundache"

app = Flask(__name__)

@app.route("/")
def main_page():
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()
    fetched = cursor.execute("SELECT * FROM recommended_songs")
    return render_template("index.html", songs=fetched.fetchall())

@app.route("/search", methods=["GET", "POST"])
def search():
    print(request.form['searchbar'])
    return "You searched: " + request.form['searchbar']

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:  # request.method = POST
        print(request.form["email"], request.form["password"])
        return "BOO"
