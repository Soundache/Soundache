from flask_sqlalchemy import SQLAlchemy
import metrohash

HASH_STR_64 = lambda s: metrohash.hash64_int(s, seed=0) // 2
db = SQLAlchemy()
