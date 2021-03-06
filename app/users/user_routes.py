import os, jwt
import clearbit
from flask import Flask, Blueprint, jsonify, request, make_response
from app import db, hunter
from app.models.models import User, Enriched
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

users = Blueprint('user', __name__)


clearbit.key = os.environ.get('CLEARBIT_KEY')

# token decorator
def token_required(f):
    """
    Token verifier decorator.
    """
    @wraps(f)
    # positional and keyword arguments
    def decorated(*args, **kwargs):
        token = None

        # x-access-token header field
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing, token required'}), 401

        # invalid tokens throw exceptions
        try:
            # decode the token and find a user that matches the id
            data = jwt.decode(token, os.environ.get('SECRET_KEY') , algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()

            if not current_user:
                return jsonify({'message': 'No user found'}), 404

        except:
            return jsonify({'message': 'Token is invalid, token required'}), 401

        # ok, if we reach here, all is good and we need to pass the user to the next middleware
        return f(current_user, *args, **kwargs)

    return decorated


# --------------------------------------------------------------
# USER ROUTES


@users.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    User route. Lists all users.
    """
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'message': 'List of all users, just a util route tbh', 'data': output})


@users.route('/user/register', methods=['POST'])
def create_user():
    """
    User route. User creation, verification and data enrichment. Reads from the body.

    Requires:

    first_name
    last_name
    email
    password
    """
    data = request.get_json()

    # verify address
    try:
        verify = hunter.email_verifier(data['email'])
        if verify.get('status') != 'valid':
            return jsonify({'message': 'Email address isn\'t verified'}), 400
    except:
        return jsonify({'message': 'Unable to verify the address'}), 500

    # try:
    # create user account
    hashed_password = generate_password_hash(str(data['password']), method='sha256')
    new_user = User(
        email=data['email'], 
        first_name=data['first_name'], 
        last_name=data['last_name'], 
        password=hashed_password
        )
    db.session.add(new_user)

    # try data enrichment
    try:
        enrich = clearbit.Enrichment.find(email=new_user.email, stream=True)

        enriched = Enriched(data=enrich, user=new_user)
        db.session.add(enriched)
    except:
        print(f'Couln\'t enrich user {new_user.email}')
        pass

    db.session.commit()

    return jsonify({'message': f'User {new_user.email} created'}), 201


@users.route('/user/login', methods=['POST'])
def login():
    """
    User route. Uses Basic auth and provides jwt tokens.

    password - provide email
    password - provide password
    """
    auth = request.authorization

    # no authorization info or partials credentials
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter_by(email=auth.username).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # if the pass checks out make a token
    # payload - public id
    # todo 30min exp too long
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
            }, os.environ.get('SECRET_KEY'))

        return jsonify({
            'message': 'Token successfully created, please include it in the <x-access-token> header',
            'data': token
            }), 201

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
