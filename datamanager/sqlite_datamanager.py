from select import select

from datamanager import DataManagerInterface
from data_models import db, User, Movie, Review

class sqlite_datamanager(DataManagerInterface.DataManagerInterface):

    def __init__(self, filename):
        self.filename = filename


    def get_all_users(self):
        """This method takes no arguments. This returns a dictionary
        of all users in the data source. Each user is represented by a dictionary."""

        return User.query.all()


    def get_user_movies(self, user_id):
        """ This method takes one argument: user_id. This represents the identifier of the user
        for whom we want to retrieve the favorite movies. Returns a dictionary of movies for the given user.
        Each movie is a dictionary with details about the movie."""
        user_movies = Movie.query.join(User).filter(int(user_id) == Movie.user_id)
        return user_movies


    def find_user_by_id(self, user_id):
        """Takes 2 arguments all_users representing all users in the storage file, and user_id.
        returns the username from the user_id"""
        selected_user = User.query.filter_by(user_id=int(user_id)).first()
        return selected_user.user_name


    def add_new_user(self, new_user):
        """Takes 2 arguments all_users representing all users in the storage file, and new_user with the
        new user ID, user name and an empty dictionary of movies.
        Adds the new user to all_users and saves it in the JSON file."""
        db.session.add(new_user)
        db.session.commit()
        return f"User has been added"



    def add_movie(self, new_movie):
        """Takes 2 arguments, user_id for the user who wants to add the movie, and the details for the new movie,
        with the following format:
        { movie_title : {
            "director": director name,
            "year": year of the movie,
            "rating": rating of the movie,
            "id": unique identifier for the movie
        }}
        """
        db.session.add(new_movie)
        db.session.commit()
        return "Movie was added"



    def update_movie(self, user_id, movie_id, updated_rating):
        """Takes 2 arguments, updated_movie in a dictionary format, and updates the movie for the user with user_id"""
        user_movies = self.get_user_movies(user_id)
        movie = Movie.query.filter_by(movie_id=movie_id).first()
        movie.rating = updated_rating
        db.session.commit()
        return "Updated correctly"



    def delete_movie(self, movie):
        """Deletes the movie from the database"""
        db.session.delete(movie)
        db.session.commit()
        return "Movie was deleted"


    def add_new_review(self, new_review):
        """Adds a review"""
        db.session.add(new_review)
        db.session.commit()
        return "Review was added"


    def get_all_reviews(self):
        """This method takes no arguments. This returns all reviews."""

        reviews = Review.query.outerjoin(User).outerjoin(Movie)
        db.session.commit()
        return reviews

    def get_all_movies(self):
        """This method takes no arguments. This returns all movies."""
        return Movie.query.all()