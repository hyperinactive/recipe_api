from flask import Flask, Blueprint, jsonify
from app import db
# todo import models when the db work starts


users = Blueprint('user', __name__)


# --------------------------------------------------------------
# USER ROUTES
@users.route('/user', methods=['GET'])
def get_all_users():
    return jsonify({'message': 'get all users'})


@users.route('/user/register', methods=['POST'])
def create_user():
    return jsonify({'message': 'register a user'})


@users.route('/user/login', methods=['POST'])
def login():
    return jsonify({'message': 'log in a user'})
