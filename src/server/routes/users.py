import re
from flask import Blueprint, jsonify, request
from flask.helpers import url_for
from werkzeug.utils import redirect
import jwt_utils
import random_address
from lib.user import User
users_bp = Blueprint('users', __name__, url_prefix='/api/user')


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')


    if not password:
        return jsonify({'message': 'password are required!'}), 400
    if not username and not email:
        return jsonify({'message': 'Username or Email and password are required!'}), 400

    user = User.login(username, password, email)
    if not user:
        return jsonify({'message': 'Invalid credentials!'}), 401

    json = user.to_json()
    if not json:
        return jsonify({'message': 'User not found!'}), 404

    json.update({
        'user_id': user.id,
        'role': 'user',
    })
    # Generate JWT token
    token = jwt_utils.encode(json)

    response = jsonify({'message': 'Login successful!'})
    response.headers['Authorization'] = f'Bearer {token}'
    response.set_cookie('authorization', f'{token}')
    return response, 200

def check_login():
    # Check if the user is logged in
    token = request.headers.get('Authorization')
    if not token:
        token = request.cookies.get("authorization")

    if not token:
        return jsonify({'message': 'Unauthorized!'}), 401
    try:
        payload = jwt_utils.decode(token)
        role = payload.get('role')
        if role != 'user':
            return jsonify({'message': 'Unauthorized!'}), 401

        return payload
    except jwt_utils.jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 401
    except jwt_utils.jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401


@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not username or not password or not email or not phone_number or not first_name or not last_name:
        return jsonify({'message': 'All fields are required!'}), 400

    # Generate random address, because we just want to test the register function
    address = random_address.real_random_address()
    if not address or len(address) == 0:
        return jsonify({'message': 'Address generation failed!'}), 500

    address_1 = address['address1']
    city = address['city']
    state = address['state']
    zip_code = address['postalCode']
    country = "US"

    user = User.register(
        username,
        password,
        email,
        first_name,
        last_name,
        phone_number,
        address_1,
        city,
        state,
        zip_code,
        country)
    if not user:
        return jsonify({'message': 'Username already exists!'}), 409

    return jsonify({'message': 'User registered successfully!'}), 201

@users_bp.route('/info', methods=['GET'])
def get_user_info():
    payload = check_login()
    if type(payload) != dict:
        return payload

    user_id = payload.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not found!'}), 400
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({'message': 'User not found!'}), 404

@users_bp.route('/forget', methods=['POST'])
def forget_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email is required!'}), 400

    user = User.get_user_by_email(email)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    signed_request = jwt_utils.encode({
        'email': email,
        'user_id': user.id,
        'request': 'forget_password'
    })
    if not signed_request:
        return jsonify({'message': 'Failed to generate signed request!'}), 500

    return redirect(f'/forget/reset?token={signed_request}&email={email}&user_id={user.id}')

@users_bp.route('/forget/reset', methods=['POST'])
def reset_password():
    signed_request = request.args.get('token')
    if not signed_request:
        return jsonify({'message': 'Token is required!'}), 400
    decoded_request = jwt_utils.decode_without_verify(signed_request)
    if not decoded_request:
        return jsonify({'message': 'Invalid token!'}), 401

    data = request.get_json()
    password = data.get('new_password')
    if not password:
        return jsonify({'message': 'New password is required!'}), 400

    email = data.get('email')
    user_id = data.get('user_id')
    user = User.get_user_by_email(email) if email else User.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    result = user.update_password(password)
    if not result:
        return jsonify({'message': 'Failed to update password!'}), 500

    return jsonify({'message': 'Password reset successfully!'}), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    payload = check_login()
    if type(payload) != dict:
        return payload

    user_id_login = payload['user_id']

    if user_id and (user_id != user_id_login):
            return jsonify({'message': 'Unauthorized!'}), 401

    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({'message': 'User not found!'}), 404
