# api.py
from flask import Blueprint, jsonify
import requests
from datamanager.sqlite_datamanager import sqlite_datamanager
from data_models import db, User, Movie, Review

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    # Implementation here
    response = requests.get("http://127.0.0.1:5000/users")
    list_of_users = []
    users = User.query.all()
    for user in users:
        user_for_list = (user.user_id, user.user_name)
        list_of_users.append(user_for_list)
    print(list_of_users)
    if len(list_of_users) > 0:
        return jsonify(list_of_users)
    else:
        return "Could not retrieve data"







