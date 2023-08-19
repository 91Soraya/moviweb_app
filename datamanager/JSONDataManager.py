import json
# from . import DataManagerInterface
from datamanager import DataManagerInterface


class JSONDataManager(DataManagerInterface.DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """This method takes no arguments. This returns a dictionary
        of all users in the data source. Each user is represented by a dictionary."""
        with open(self.filename, "r") as handle:
            data = json.load(handle)
            all_users = {}
            for user in data:
                user_id = (int(str(user)))
                user_name = data[user]["name"]
                all_users[user_id] = user_name
            return all_users

    def get_user_movies(self, user_id):
        """ This method takes one argument: user_id. This represents the identifier of the user
        for whom we want to retrieve the favorite movies. Returns a dictionary of movies for the given user.
        Each movie is a dictionary with details about the movie."""
        with open(self.filename, "r") as handle:
            data = json.load(handle)
            try:
                return data[str(user_id)]["movies"]
            except KeyError:
                return "User ID not found"

    def find_user_by_id(self, all_users, user_id):
        """Takes 2 arguments all_users representing all users in the storage file, and user_id.
        returns the username from the user_id"""
        for user in all_users:
            if user == user_id:
                return all_users[user]
            else:
                continue
        return "User ID not found"

    def add_new_user(self, new_user):
        """Takes 2 arguments all_users representing all users in the storage file, and new_user with the
        new user ID, user name and an empty dictionary of movies.
        Adds the new user to all_users and saves it in the JSON file."""
        users = {}
        with open(self.filename, "r") as handle:
            data = json.load(handle)
            users = data
        users.update(new_user)
        json_str = json.dumps(users)
        with open(self.filename, "w") as handle:
            handle.write(json_str)
        handle.close()
        return "User has been added"

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
        with open(self.filename, "r") as handle:
            data = json.load(handle)
            users = data
            users[user_id]["movies"].update(new_movie)
        json_str = json.dumps(users)
        with open(self.filename, "w") as handle:
            handle.write(json_str)
        handle.close()
        return "Movie has been added"

    def get_movie_details(self, user_movies, movie_id):
        """Get all movie details for a specific movie"""
        for movie in user_movies:
            print(movie)
        return movie

    def update_movie(self, user_id, movie_id):
        pass


