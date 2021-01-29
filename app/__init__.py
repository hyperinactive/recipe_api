from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pyhunter import PyHunter
from dotenv import load_dotenv
import os


load_dotenv()
db = SQLAlchemy()
hunter = PyHunter(os.environ.get('HUNTER_API_KEY'))

# create an app instance
def create_app(config_class=None):
    """
    Inits an app instance.
    """
    app = Flask(__name__)
    # app.config.from_object(Config)

    # config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_CLOUD')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)

    # import blueprints
    from app.users.user_routes import users
    from app.recipes.recipe_routes import recipes
    from app.ingredients.ingredient_routes import ingredients

    # register blueprints
    app.register_blueprint(users)
    app.register_blueprint(recipes)
    app.register_blueprint(ingredients)

    return app