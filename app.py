from flask import Flask, render_template, request, redirect, url_for
from jinja2 import UndefinedError

from datamanager.JSONDataManager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users.json')  # Use the appropriate path to your JSON file


def create_new_id():
    user_ids = []
    users = data_manager.get_all_users()
    for user_id in users:
        user_ids.append(user_id)
    max_id = int(max(user_ids)) + 1
    return max_id


def create_new_user(name, user_id):
    new_user = {str(user_id): {
        "name": name,
        "movies": {}
    }}
    return new_user


@app.route('/')  # Home page
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')  # present a list of all users registered in our MovieWeb App.
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route("/users/<user_id>")  # exhibit a specific user’s list of favorite movies.
def list_favorite_movies(user_id):
    users = data_manager.get_all_users()
    user_name = data_manager.find_user_by_id(users, int(user_id))
    user_movies = data_manager.get_user_movies(user_id)
    try:
        return render_template('user_movies.html', users=users, user_name=user_name, user_movies=user_movies,
                               user_id=user_id)
    except UndefinedError:
        error_message = "User ID could not be found."
        return render_template("not_found.html", error_message=error_message)


@app.route("/add_user", methods=["GET", "POST"])  # Present a form that enables the addition of a new user
def add_new_user():
    if request.method == "POST":
        name = request.form.get("name")
        existing_users = data_manager.get_all_users()
        for user in existing_users:
            if name.lower() == existing_users[user].lower():
                error_message = "User already exists."
                return render_template("error.html", error_message=error_message)
        user_id = create_new_id()
        new_user = create_new_user(name, user_id)
        data_manager.add_new_user(new_user)
        return redirect(url_for("list_users"))
    return render_template("add_user.html")


@app.route("/users/<user_id>/add_movie")  # Display a form to add a new movie to a user´s list of favorite movies
def add_movie():
    pass


@app.route("/users/<user_id>/update_movie/movie_id")  # display a form allowing for the updating of details of a specific movie in a user’s list.
def update_movie():
    pass


@app.route("/users/<user_id>/delete_movie/<movie_id>")  # Upon visiting this route, a specific movie will be removed from a user’s favorite movie list.
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(debug=True)
