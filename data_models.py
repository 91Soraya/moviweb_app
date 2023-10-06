from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)


class Director(db.Model):
    __tablename__ = "directors"
    director_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(50))


class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.director_id"))


class AppMovie(db.Model):
    __tablename__ = "App-movies"
    app_movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    title = db.Column(db.String(50), unique=True)
