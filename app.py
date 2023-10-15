from flask import Flask, render_template, request, redirect, url_for
from jinja2 import UndefinedError
import requests
import json
from data_models import db, User, Movie

from datamanager.JSONDataManager import JSONDataManager
from datamanager.sqlite_datamanager import sqlite_datamanager

app = Flask(__name__)
#data_manager = JSONDataManager('datamanager/users.json')  # Use the appropriate path to your JSON file
data_manager = sqlite_datamanager('data/library.sqlite')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}\data\library.sqlite"
db.init_app(app)

#with app.app_context():
#    db.create_all()

def create_new_user_id():
    user_ids = []
    users = data_manager.get_all_users()
    for user_id in users:
        user_ids.append(user_id)
    if len(user_ids) < 1:
        return 1
    else:
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
    user_name = data_manager.find_user_by_id(user_id)
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
            if name.lower() == user.user_name.lower():
                error_message = "User already exists."
                return render_template("error.html", error_message=error_message)
        new_user = User(user_name=name)
        data_manager.add_new_user(new_user)
        return redirect(url_for("list_users"))
    return render_template("add_user.html")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])  # Display a form to add a new movie to a user´s list
def add_movie(user_id):
    if request.method == "POST":
        movie_title = request.form.get("movie_title")
        try:
            response_api = requests.get("http://www.omdbapi.com/?apikey=4220af53&t=" + movie_title)
        except requests.exceptions.HTTPError:
            error_message = "Http Error"
            print(error_message)
            return render_template("error.html", error_message=error_message)
        except requests.exceptions.ConnectionError:
            error_message = "Connection Error"
            print(error_message)
            return render_template("error.html", error_message=error_message)
        except requests.exceptions.Timeout:
            error_message = "Timeout Error"
            print(error_message)
            return render_template("error.html", error_message=error_message)
        except requests.exceptions.RequestException:
            error_message = "Oops, something went wrong"
            print(error_message)
            return render_template("error.html", error_message=error_message)

        api_data = response_api.text
        parse_json = json.loads(api_data)
        if parse_json["Response"] == "False":
            error_message = "Parsing error"
            return render_template("error.html", error_message=error_message)
        else:
            director = parse_json["Director"]
            year = int(parse_json["Year"])
            rating = float(parse_json["imdbRating"])
            print(user_id)
            new_movie = Movie(user_id=int(user_id), title=movie_title, year=year, director=director, rating=rating)
            data_manager.add_movie(new_movie)
            return redirect(url_for("list_users"))

    return render_template("add_movie.html", user_id=user_id)


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
# display a form allowing for the updating of details of a specific movie in a user’s list.
def update_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    for movie in user_movies:
        if int(movie_id) == int(movie.movie_id):
            movie_title = movie.title
            rating = movie.rating
    if request.method == "POST":
        updated_rating = float(request.form.get("rating"))
        data_manager.update_movie(user_id, movie_id, updated_rating)
        return redirect(url_for("list_favorite_movies", user_id=user_id))
    return render_template("update_movie.html", user_movies=user_movies, movie_id=movie_id, movie_title=movie_title,
                           rating=rating, user_id=user_id)


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET", "POST"])
# Upon visiting this route, a specific movie will be removed from a user’s favorite movie list.
def delete_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    for movie in user_movies:
        if int(movie_id) == int(movie.movie_id):
            print("Matching movie_id")
            data_manager.delete_movie(movie)

    return redirect(url_for("list_favorite_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
