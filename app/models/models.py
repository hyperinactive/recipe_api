from app import db
from flask import Blueprint
from datetime import datetime


# --------------------------------------------------------------
# MODELS


# association table recipes_rated
# reviewers - User <-> Recipe
user_reviews = db.Table('user_reviews',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
)

# association table ingredients used
# ingredients_used - Recipe <-> Ingredient
ingredients_used = db.Table('ingredients_used',
    db.Column('recepe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')),
)


# User -> Recipe
# creation: One -> Many
# reating: Many -> Many
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # lazy load when necessary, author ref
    recipes_created = db.relationship('Recipe', backref='author', lazy=True)
    # though declared here, it actually resides in the Recipe model
    recipes_rated = db.relationship('Recipe', secondary=user_reviews, backref=db.backref('reviewers', lazy='dynamic'))

    def __repr__(self):
        return f'User("{self.first_name}"), ("{self.last_name}"), ("{self.email}")'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    average_rating = db.Column(db.Float, default=0)
    rating_points = db.Column(db.Integer, default=0)
    rating_count = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f'Recipe("{self.name}"), ("{self.text}"), ("{self.rating}"), ("{self.user_id}")'


# Recipe -> Ingredient
# used: Many -> Many
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    used = db.relationship('Recipe', secondary=ingredients_used, backref=db.backref('used', lazy='dynamic'))


    def __repr__(self):
        return f'Ingredient("{self.name}")'
