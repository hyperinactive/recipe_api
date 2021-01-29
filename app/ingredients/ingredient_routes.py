from flask import Flask, Blueprint, jsonify
from app import db
from app.users.user_routes import token_required
from app.models.models import Recipe, Ingredient, ingredients_used
from sqlalchemy import func, desc

ingredients = Blueprint('ingredients', __name__)


# --------------------------------------------------------------
# INGREDIENT ROUTES


@ingredients.route('/ingredient', methods=['GET'])
@token_required
def get_top_ingredients(current_user):
    """
    Ingredient route. Returns top 5 most used ingredients.
    """
    top_ingredients = Ingredient.query.join(Recipe.used).group_by(Ingredient.id).order_by(desc(func.count(Ingredient.id))).limit(5)
    # top 5 most used ingredients
    
    # select ingredient_id, count(ingredient_id) from ingredients_used
    # group by ingredient_id
    # order by count(ingredient_id) desc
    # limit 5;
    
    output = []

    for ingredient_item in top_ingredients:
        ingredient_obj = {}
        ingredient_obj['name'] = ingredient_item.name
        output.append(ingredient_obj)

    return jsonify({'message': 'Top 5 most used ingredients' , 'data': output})
