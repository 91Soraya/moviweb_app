from flask import Flask, render_template, request
from datamanager.JSONDataManager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users.json')  # Use the appropriate path to your JSON file

@app.route('/') # Home page
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users') # present a list of all users registered in our MovieWeb App.
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route("/users/<user_id>") # exhibit a specific user’s list of favorite movies.
def list_favorite_movies(user_id):
    users = data_manager.get_all_users()
    user_name = data_manager.find_user_by_id(users, int(user_id))
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', users=users, user_name=user_name, user_movies=user_movies, user_id=user_id)

@app.route("/add_user") # Present a form that enables the addition of a new user to our moviweb app
def add_new_user():
    pass

@app.route("/users/<user_id>/add_movie") # Display a form to add a new movie to a user´s list of favorite movies
def add_movie():
    pass

@app.route("/users/<user_id>/update_movie/movie_id") # display a form allowing for the updating of details of a specific movie in a user’s list.
def update_movie():
    pass

@app.route("/users/<user_id>/delete_movie/<movie_id>") # Upon visiting this route, a specific movie will be removed from a user’s favorite movie list.
def delete_movie():
    pass

if __name__ == '__main__':
    app.run(debug=True)
