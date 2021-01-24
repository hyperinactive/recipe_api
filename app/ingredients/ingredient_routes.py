from flask import Flask, Blueprint, jsonify
from app import db
# todo import models when the db work starts


ingredients = Blueprint('ingredients', __name__)


# --------------------------------------------------------------
# INGREDIENT ROUTES


@ingredients.route('/ingredient', methods=['GET'])
def get_top_ingredients():
    return jsonify({'message': 'top 5 ingredients'})
