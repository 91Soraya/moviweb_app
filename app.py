from flask import Flask, render_template, request, redirect, url_for
from jinja2 import UndefinedError

from datamanager.JSONDataManager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users.json')  # Use the appropriate path to your JSON file


def create_new_user_id():
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


def create_new_movie_id():
    all_movie_ids = []
    all_users = data_manager.get_all_users()
    for user in all_users:
        user_movies = data_manager.get_user_movies(user)
        for movie in user_movies:
            all_movie_ids.append(user_movies[movie]["movie_id"])
    highest_id = max(all_movie_ids)
    return highest_id + 1


@app.route('/')  # Home page
def home():
    return render_template("index.html")


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
        if len(name) < 2:
            error_message = "Please enter name of minimum 2 characters."
            return render_template("error.html", error_message=error_message)
        existing_users = data_manager.get_all_users()
        for user in existing_users:
            if name.lower() == existing_users[user].lower():
                error_message = "User already exists."
                return render_template("error.html", error_message=error_message)
        user_id = create_new_user_id()
        new_user = create_new_user(name, user_id)
        data_manager.add_new_user(new_user)
        return redirect(url_for("list_users"))
    return render_template("add_user.html")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])  # Display a form to add a new movie to a user´s list
def add_movie(user_id):
    if request.method == "POST":
        movie_title = request.form.get("movie_title")
        director = request.form.get("director")
        year = int(request.form.get("year"))
        rating = float(request.form.get("rating"))
        movie_id = create_new_movie_id()
        new_movie = {movie_title: {
            "director": director,
            "year": year,
            "rating": rating,
            "movie_id": movie_id
        }}
        data_manager.add_movie(user_id, new_movie)
        return redirect(url_for("list_users"))
    return render_template("add_movie.html", user_id=user_id)


@app.route("/users/<user_id>/update_movie/<movie_id>")
# display a form allowing for the updating of details of a specific movie in a user’s list.
def update_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    for movie in user_movies:
        if int(movie_id) == int(user_movies[movie]["movie_id"]):
            movie_title = movie
            year = user_movies[movie]["year"]
            director = user_movies[movie]["director"]
            rating = user_movies[movie]["rating"]

    return render_template("update_movie.html", user_movies=user_movies, movie_id=movie_id, movie_title=movie_title,
                           year=year, director=director, rating=rating)


@app.route("/users/<user_id>/delete_movie/<movie_id>")
# Upon visiting this route, a specific movie will be removed from a user’s favorite movie list.
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(debug=True)
