from flask import Flask, Blueprint, jsonify, request
from app import db
from app.users.user_routes import token_required
from app.models.models import Recipe, User, Ingredient

recipes = Blueprint('recipes', __name__)


# --------------------------------------------------------------
# RECIPE ROUTES


@recipes.route('/recipe', methods=['GET'])
def get_all_recipes():
    return jsonify({'message': 'get all recipes'})


@recipes.route('/recipe', methods=['POST'])
@token_required
def create_recipe(current_user):
    return jsonify({'message': 'create a recipe'})


# todo need no user id, identify users via JWT!?
@recipes.route('/recipe/<int:user_id>', methods=['GET'])
def get_user_recipes(user_id):
    return jsonify({'message': 'get user recipes'})


@recipes.route('/recipe/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    return jsonify({'message': 'rate a recipe'})
