from app import db
from flask import Blueprint
from datetime import datetime


# --------------------------------------------------------------
# MODELS


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # lazy load when necessary, author ref
    recipes_created = db.relationship('Recipe', backref='author', lazy=True)
    recipes_rated = db.relationship('Recipe', backref='rated', lazy=True)

    def __repr__(self):
        return f'User("{self.first_name}"), ("{self.last_name}"), ("{self.email}")'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    def __repr__(self):
        return f'Recipe("{self.name}"), ("{self.text}"), ("{self.rating}"), ("{self.user_id}")'


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    times_used = db.Column(db.Integer, default=0)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f'Ingredient("{self.name}"), ("{self.times_used}"), ("{self.recipe_id}")'
