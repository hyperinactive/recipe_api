from flask import Flask, Blueprint, jsonify
from app import db
# todo import models when the db work starts


recipes = Blueprint('recipes', __name__)


# --------------------------------------------------------------
# RECIPE ROUTES


@recipes.route('/recipe', methods=['GET'])
def get_all_recipes():
    return jsonify({'message': 'get all recipes'})


@recipes.route('/recipe', methods=['POST'])
def create_recipe():
    return jsonify({'message': 'create a recipe'})


# todo need no user id, identify users via JWT!?
@recipes.route('/recipe/<int:user_id>', methods=['GET'])
def get_user_recipes(user_id):
    return jsonify({'message': 'get user recipes'})


@recipes.route('/recipe/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    return jsonify({'message': 'rate a recipe'})
