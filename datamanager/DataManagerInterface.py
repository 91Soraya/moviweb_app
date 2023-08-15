from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """This method takes no arguments. This method should return a dictionary
        of all users in our data source. Each user is represented by a dictionary."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """ This method takes one argument: user_id. This represents the identifier of the user
        for whom we want to retrieve the favorite movies. Returns a dictionary of movies for the given user.
        Each movie is a dictionary with details about the movie."""
        pass

    @abstractmethod
    def find_user_by_id(self, users, user_id):
        """Takes 2 arguments all_users representing all users in the storage file, and user_id.
        returns the username from the user_id"""
        pass

    @abstractmethod
    def add_new_user(self, new_user):
        """Takes 2 arguments all_users representing all users in the storage file, and new_user with the
        new user ID, user name and an empty dictionary of movies.
        Adds the new user to all_users and saves it in the JSON file."""
        pass

    def add_movie(self, user_id, new_movie):
        """Takes 2 arguments, user_id for the user who wants to add the movie, and the details for the new movie,
        with the following format:
        { movie_title : {
            "director": director name,
            "year": year of the movie,
            "rating": rating of the movie,
            "id": unique identifier for the movie
        }}
        """
        pass
