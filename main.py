from datamanager.JSONDataManager import JSONDataManager

json_object = JSONDataManager("datamanager/users.json")
favorite_movies = json_object.get_user_movies(2)
for movie in favorite_movies:
    print(favorite_movies[movie]["year"])

json_users = json_object.get_all_users()

print(json_object.find_user_by_id(json_users, 2))