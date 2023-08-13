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
