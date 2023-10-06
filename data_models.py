from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True)
    birth_date = db.Column(db.String, nullable=False)


class Director(db.Model):
    __tablename__ = "directors"
    director_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    director_name = db.Column(db.String(50))
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String)


class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.director_id"))
    imbd_rating = db.Column(db.Float)


class UserMovie(db.Model):
    __tablename__ = "User_movie_records"
    user_movie_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    rating = db.Column(db.Float)
    title = db.Column(db.String(50), unique=True)


"""
Now, if you want to retrieve all movies from the database, with SQLAlchemy ORM, it would look something like this:

movies = db.session.query(Movie).all()
for movie in movies:
    print(movie.title)
"""
