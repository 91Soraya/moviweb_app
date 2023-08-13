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


# json_object = JSONDataManager("users.json")
# print(json_object.get_all_users())
# print(json_object.get_user_movies(2))
# users = json_object.get_all_users()
# print(json_object.find_user_by_id(users, 2))
