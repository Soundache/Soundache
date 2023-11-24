from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, LargeBinary, BINARY

NAME = "Soundache Song Database"

app = Flask(NAME)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///songs.db"
db = SQLAlchemy()
db.init_app(app)

class Song(db.Model):
    name: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artistID: Mapped[int] = mapped_column(Integer)
    # thumbnail: Mapped = mapped_column(LargeBinary, nullable=True)
    # midi = mapped_column(LargeBinary)
    # lyrics = mapped_column(LargeBinary)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8000)