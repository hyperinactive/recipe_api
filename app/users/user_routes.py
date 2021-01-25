from flask import Flask, Blueprint, jsonify, request, make_response
from app import db
from app.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('user', __name__)

# --------------------------------------------------------------
# USER ROUTES
@users.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users': output})


@users.route('/user/register', methods=['POST'])
def create_user():
    data = request.get_json()

    try:
        hashed_password = generate_password_hash(str(data['password']), method='sha256')
        new_user = User(
            email=data['email'], 
            first_name=data['first_name'], 
            last_name=data['last_name'], 
            password=hashed_password
            )

        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({'message': 'Invalid or missing fields'}), 400

    return jsonify({'message': f'User {new_user.email} created'}), 201


@users.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    if check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Successfully logged in'})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
