from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True)

    def __init__(self, user_name):
        self.user_name = user_name


class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    director = db.Column(db.String)
    rating = db.Column(db.Float)

    def __init__(self, title, year, rating, user_id, director):
        self.title = title
        self.year = year
        self.director = director
        self.rating = rating
        self.user_id = user_id


"""
Now, if you want to retrieve all movies from the database, with SQLAlchemy ORM, it would look something like this:

movies = db.session.query(Movie).all()
for movie in movies:
    print(movie.title)
"""
