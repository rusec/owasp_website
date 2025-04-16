from flask import Blueprint, jsonify, request
import jwt_utils
import server.database.users as user_db 
import server.database.login as login_db
import random_address

users_bp = Blueprint('users', __name__, url_prefix='/api/user')


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password and type(username) != str and type(password) != str:
        return jsonify({'message': 'Username and password are required!'}), 400
    
    
    if login_db.login_user(username, password) == False:
        return jsonify({'message': 'Invalid credentials!'}), 401
    
    user = user_db.get_user(username)
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    

    # Generate JWT token
    token = jwt_utils.encode({
        'username': username ,
        "user_id": user['id'],
        'role': 'user',
    })


    request.headers['Authorization'] = f'Bearer {token}'
    request.cookies['Authorization'] = f'Bearer {token}'


    return jsonify({'token': token}), 200

def check_login():
    # Check if the user is logged in
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'message': 'Unauthorized!'}), 401
    try:
        payload = jwt_utils.decode(token)
        role = payload['role']
        if role != 'user':
            return jsonify({'message': 'Unauthorized!'}), 401

        return payload
    except jwt_utils.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'}), 401
    except jwt_utils.InvalidTokenError:
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


    # Generate random address, because we just want to test the register function
    address = random_address.real_random_address_by_city('New Brunswick')
    address_1 = address['address1']
    city = address['city']
    state = address['state']
    zip_code = address['zip']
    country = address['country']


    if not username or not password or not email or not phone_number or not first_name or not last_name:
        return jsonify({'message': 'All fields are required!'}), 400

    if user_db.register_user(
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
        country
        ) == False:
        return jsonify({'message': 'Username already exists!'}), 409
    
    return jsonify({'message': 'User registered successfully!'}), 201

@users_bp.route('/', methods=['GET'])
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user():
    payload = check_login()
    if type(payload) != dict:
        return payload
    
    user_id = payload['user_id']
    username_args = request.view_args.get('user_id')
    if username_args and username_args != user_id:
            return jsonify({'message': 'Unauthorized!'}), 401
    
    user = user_db.get_user_by_id(username_args or user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found!'}), 404
    
