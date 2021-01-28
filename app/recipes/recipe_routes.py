from flask import Flask, Blueprint, jsonify, request
from app import db
from app.users.user_routes import token_required
from app.models.models import Recipe, User, Ingredient, ingredients_used
from sqlalchemy import and_, desc, func, inspect

recipes = Blueprint('recipes', __name__)


# --------------------------------------------------------------
# RECIPE ROUTES


@recipes.route('/recipe', methods=['GET'])
@token_required
def get_all_recipes(current_user):
    # default query
    query = Recipe.query.join(Recipe.used).group_by(Recipe.id)

    # get query string
    query_string = request.args

    # filters
    name_keyword = query_string.get('name')
    text_keyword = query_string.get('text')
    ingredient_keyword_list = query_string.getlist('ingredient')

    # order
    order_keyword = query_string.get('order')

    # go through args
    if name_keyword:
        query = query.filter(Recipe.name.ilike(f'%{name_keyword}%'))
    if text_keyword:
        query = query.filter(Recipe.text.ilike(f'%{text_keyword}%'))
    if ingredient_keyword_list and len(ingredient_keyword_list) != 0:
        print('ingredients found')

        for item in ingredient_keyword_list:
            item.lower()

        # query = query.join(Ingredient.used).group_by(Recipe.id)

        # for ingredient in ingredient_keyword_list:
        #     query_tmp = query.filter(Ingredient.name.ilike(f'%{ingredient}%'))
        #     print(ingredient)
        #     # query = query.filter(Ingredient.name.ilike(f'%{ingredient}%'))
        #     query = query.intersect(query_tmp)
        #     print(query.all())
        #     print(query_tmp.all())

    # order the query
    if order_keyword:

        if order_keyword == 'max_ing':
            """
            filter recipes by ingredients used

            select recipe_id, count(ingredient_id) from ingredients_used
            group by recipe_id
            order by count(ingredient_id) <desc - asc>
            """
            query = query.order_by(desc(func.count(Ingredient.id))) 
        else:
            query = query.order_by(func.count(Ingredient.id))


    query = query.all()
    if len(query) == 0:
        return jsonify({'message': 'No recipes found'}), 204

    output = []
    for recipe in query:
        recipe_obj = {}
        recipe_obj['name'] = recipe.name
        recipe_obj['average_rating'] = recipe.average_rating
        recipe_obj['text'] = recipe.text
        recipe_obj['author'] = recipe.author.email
        recipe_obj['ingredients'] = []

        for ingredient in recipe.used:
            recipe_obj['ingredients'].append(ingredient.name)
            
        output.append(recipe_obj)

    return jsonify(output)


@recipes.route('/recipe', methods=['POST'])
@token_required
def create_recipe(current_user):
    data = request.get_json()

    try:
        for item in data:
            new_recipe = Recipe(
                name=item['name'],
                text=item['text'],
                author=current_user
            )
            for ingredient_item in item['ingredients']:
                # check for an existing ingredient
                new_ingredient = Ingredient.query.filter(Ingredient.name.ilike(ingredient_item)).first()
                if not new_ingredient:
                    new_ingredient = Ingredient(name=ingredient_item)
                    db.session.add(new_ingredient)
                    db.session.commit()

                # either way create a relationship
                new_recipe.used.append(new_ingredient)
                
            db.session.commit()
    except:
        return jsonify({'message': 'Invalid or missing attributes'}), 400


    return jsonify({'message': 'Recipe/s successfully created'})


@recipes.route('/recipe/mine', methods=['GET'])
@token_required
def get_user_recipes(current_user):
    own_recipes = Recipe.query.filter_by(author_id=current_user.id).all()

    output = []
    for recipe in own_recipes:
        recipe_obj = {}
        recipe_obj['name'] = recipe.name
        recipe_obj['average_rating'] = recipe.average_rating
        recipe_obj['text'] = recipe.name
        recipe_obj['author'] = recipe.author.email
        recipe_obj['ingredients'] = []

        for ingredient in recipe.used:
            recipe_obj['ingredients'].append(ingredient.name)
            
        output.append(recipe_obj)
        

    return jsonify(output)


@recipes.route('/recipe/<int:recipe_id>', methods=['POST'])
@token_required
def rate_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe.author_id == current_user.id or current_user in recipe.reviewers:
        return jsonify({'message': 'Cannot rate your own recipes or rate one recipe multiple times'}), 403

    rating = request.get_json()['rating']
    if rating not in range(1,6):
        return jsonify({'message': 'Rating must be 1-5'}), 401

    # update the rating
    recipe.rating_points += rating
    recipe.rating_count += 1
    recipe.average_rating = recipe.rating_points / recipe.rating_count

    recipe.reviewers.append(current_user)

    db.session.commit()

    return jsonify({'message': f'Recipe {recipe.name} successfully rated: {rating}'}), 201


# @recipes.route('/recipe/min_max')
# def get_min_max_recipes():
#     """
#     filter recipes by ingredients used

#     select recipe_id, count(ingredient_id) from ingredients_used
#     group by recipe_id
#     order by count(ingredient_id) <desc - asc>
#     """

#     max_ingredients = Recipe.query.join(Recipe.used).group_by(Recipe.id).order_by(desc(func.count(Ingredient.id))).all()

#     output = []
#     for recipe in max_ingredients:
#         recipe_obj = {}
#         recipe_obj['name'] = recipe.name
#         recipe_obj['average_rating'] = recipe.average_rating
#         recipe_obj['ingredients'] = []
#         for ingredient in recipe.used:
#             recipe_obj['ingredients'].append(ingredient.name)
#         output.append(recipe_obj)

#     return jsonify({'max': output})
