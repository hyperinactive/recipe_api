import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# CONFIG
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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


@app.route('/')
def home():
    return 'sanity check'


if __name__ == '__main__':
    app.run(debug=True)
