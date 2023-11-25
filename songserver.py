from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, LargeBinary, BINARY
import toml

NAME = "Soundache Song Database"
SECRETS = toml.load('instance/secrets.toml')

app = Flask(NAME)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
app.secret_key = SECRETS['secret_key']   # secrets.token_hex()
db = SQLAlchemy()
db.init_app(app)

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer)
    # thumbnail: Mapped = mapped_column(LargeBinary, nullable=True)
    # midi = mapped_column(LargeBinary)
    # lyrics = mapped_column(LargeBinary)

@app.route("/upload", )
def upload():
    return jsonify(), 200

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8000)