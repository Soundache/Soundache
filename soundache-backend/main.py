from flask import Flask, render_template, url_for, send_from_directory, send_file
import sqlite3

SOUNDACHE = "Soundache"

app = Flask(__name__)

@app.route("/")
def main_page():
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()
    fetched = cursor.execute("SELECT * FROM recommended_songs")
    return render_template("index.html", songs=fetched.fetchall())
